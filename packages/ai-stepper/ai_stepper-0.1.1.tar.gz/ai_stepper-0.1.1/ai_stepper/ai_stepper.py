from litellm import completion
from pydantic import BaseModel, ValidationError
from yaml import safe_load
from typing import Dict, Any, Optional, Union, Type, Callable
from .schema.step import Step
from .schema.output_validation_error import OutputValidationError
import os
import json
import re
from datetime import datetime
from jsonschema import validate, ValidationError
from jsonschema.exceptions import SchemaError

class AI_Stepper:
    def __init__(self, llm_base_url: str, llm_api_key: str, llm_model_name: str):
        self.llm_model_name = llm_model_name
        self.llm_base_url = llm_base_url
        self.llm_api_key = llm_api_key
        self.context = {}
        self.type_map = {
            "string": str,
            "integer": int,
            "float": float,
            "number": (int, float),
            "boolean": bool,
            "array": list,
            "object": dict,
            "dict": dict,
            "any": object
        }

    def load_steps(self, steps_file: str, initial_inputs: Dict[str, Any]) -> Dict[str, Step]:
        """
        Loads steps from a YAML file, converts schemas to JSON Schema inline, and verifies that all required inputs are provided
        or produced by previous steps.

        Args:
            steps_file (str): Path to the YAML file.
            initial_inputs (Dict[str, Any]): Inputs provided at the start of the workflow.

        Returns:
            Dict[str, Step]: A dictionary of step names to Step objects.

        Raises:
            ValueError: If a required input is missing and not produced by previous steps.
        """
        type_map = {
            "string": {"type": "string"},
            "integer": {"type": "integer"},
            "float": {"type": "number"},
            "number": {"type": "number"},
            "boolean": {"type": "boolean"},
            "array": {"type": "array", "items": {"type": "any"}},
            "object": {"type": "object"},
            "dict": {"type": "object"},
            "any": {}
        }

        def to_jsonschema(schema):
            if isinstance(schema, str):
                return type_map.get(schema, {})
            if isinstance(schema, dict):
                if "type" in schema:
                    # Handle array schema
                    if schema["type"] == "array" and "items" in schema:
                        return {
                            "type": "array",
                            "items": to_jsonschema(schema["items"])
                        }
                    # Return schema as-is if already JSON Schema-like
                    return schema
                # Handle properties for objects
                if "properties" in schema:
                    return {
                        "type": "object",
                        "properties": {
                            key: to_jsonschema(value)
                            for key, value in schema["properties"].items()
                        }
                    }
            raise ValueError("Invalid schema format.")

        try:
            with open(steps_file, "r", encoding="utf-8") as f:
                steps_dict = safe_load(f)

            # Track available inputs as we process steps
            available_inputs = set(initial_inputs.keys())

            # Validate each step
            for step_name, step_data in steps_dict.items():
                # Convert step outputs to JSON Schema format
                if "outputs" in step_data:
                    step_data["outputs"] = {
                        key: to_jsonschema(schema)
                        for key, schema in step_data["outputs"].items()
                    }

                # Validate that all required inputs for this step are available
                if "inputs" in step_data:
                    missing_inputs = [
                        input_key for input_key in step_data["inputs"].keys()
                        if input_key not in available_inputs
                    ]
                    if missing_inputs:
                        raise ValueError(
                            f"Step '{step_name}' requires missing inputs: {', '.join(missing_inputs)}. "
                            f"Ensure these inputs are provided as initial inputs or produced by previous steps."
                        )

                # Add step outputs to available inputs for subsequent steps
                if "outputs" in step_data:
                    available_inputs.update(step_data["outputs"].keys())

            return {name: Step(**data) for name, data in steps_dict.items()}
        except (ValidationError, Exception) as e:
            raise Exception(f"Failed to load steps: {e}")

    def format_task(self, task: str, context: Dict[str, Any]) -> str:
        for key, value in context.items():
            placeholder = f"{{{key}}}"
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            task = task.replace(placeholder, str(value))
        unresolved = re.findall(r"{\w+}", task)
        if unresolved:
            print(f"[DEBUG] Unresolved placeholders: {unresolved}")
        return task

    def clean_response(self, response: str) -> str:
        """
        Cleans the LLM response by removing code block enclosures and extra text.
        Attempts to find and extract valid JSON from the response.
        """
        # First try to extract JSON from code blocks
        code_block_match = re.search(r'```(?:json)?\n?([\s\S]*?)\n?```', response, flags=re.IGNORECASE)
        if code_block_match:
            return code_block_match.group(1).strip()

        # If no code blocks, try to find JSON object or array pattern
        json_pattern = r'(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\])'
        json_match = re.search(json_pattern, response)
        if json_match:
            return json_match.group(1).strip()

        # If no JSON patterns found, return the stripped response
        return response.strip()

    def validate_output(self, output: Any, schema: Dict[str, Any]) -> Any:
        """
        Validates the given output against a JSON Schema.
        
        Args:
            output (Any): The actual output to validate.
            schema (Dict[str, Any]): The JSON Schema to validate against.
        
        Returns:
            Any: The validated output if it conforms to the schema.

        Raises:
            OutputValidationError: If the output does not conform to the schema.
        """
        try:
            validate(instance=output, schema=schema)
            return output  # Return the validated output unchanged
        except ValidationError as e:
            raise OutputValidationError(f"Validation error: {e.message}")
        except SchemaError as e:
            raise OutputValidationError(f"Schema error: {e.message}")

    def query_llm(
        self,
        prompt: str,
        expected_outputs: Dict[str, Any],
        max_retries: int,
        callback: Optional[Callable[[str, Optional[str]], None]],
        step_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        attempts_history = []  # List to store all attempts and their errors
        for attempt in range(max_retries):
            try:
                current_prompt = prompt
                if attempts_history:
                    error_context = "\nYour previous attempts failed the validation check:\n"
                    for i, (error, response) in enumerate(attempts_history, 1):
                        error_context += f"\nAttempt {i}:\n"
                        error_context += f"Error: {error.strip()}\n"
                        error_context += f"Your previous generation: {response.strip()}\n"
                    error_context += "\nPlease fix the output to match the expected schema exactly."
                    current_prompt = f"{prompt}{error_context}"

                if callback:
                    callback(f"LLM INPUT:\n{current_prompt}", step_name)

                try:
                    response = completion(
                        messages=[{"role": "user", "content": current_prompt}],
                        base_url=self.llm_base_url,
                        api_key=self.llm_api_key,
                        model=self.llm_model_name
                    )
                    content = response.choices[0].message.content.strip()
                except Exception as e:
                    if attempt < max_retries - 1:
                        if callback:
                            callback(f"LLM ERROR: {str(e)}. Retrying...", step_name)
                        continue
                    raise

                cleaned_content = self.clean_response(content)

                if callback:
                    callback(f"LLM OUTPUT: {cleaned_content}", step_name)

                try:
                    parsed_output = json.loads(cleaned_content)
                except json.JSONDecodeError as e:
                    error = f"Invalid JSON format: {str(e)}"
                    if attempt < max_retries - 1:
                        if callback:
                            callback(f"Failed to parse JSON: {error}. Retrying...", step_name)
                        attempts_history.append((error, cleaned_content))
                        continue
                    raise OutputValidationError(error)

                # Validate and convert output
                if len(expected_outputs) == 1:
                    output_name = list(expected_outputs.keys())[0]
                    try:
                        validated_output = self.validate_output(parsed_output[output_name], expected_outputs[output_name])
                        if callback:
                            callback(f" Validated output '{output_name}' successfully", step_name)
                        return {output_name: validated_output}
                    except KeyError:
                        error = f"Missing required key '{output_name}' in response. Response keys: {list(parsed_output.keys())}"
                        attempts_history.append((error, cleaned_content))
                        if attempt < max_retries - 1:
                            if callback:
                                callback(f"Validation failed: {error}. Retrying...", step_name)
                            continue
                        raise OutputValidationError(error)

                elif isinstance(parsed_output, dict):
                    result = {}
                    try:
                        for key, schema in expected_outputs.items():
                            if key not in parsed_output:
                                error = f"Missing required key '{key}' in response. Available keys: {list(parsed_output.keys())}"
                                attempts_history.append((error, cleaned_content))
                                raise OutputValidationError(error)
                            result[key] = self.validate_output(parsed_output[key], schema)
                            if callback:
                                callback(f" Validated output '{key}' successfully", step_name)
                        return result
                    except OutputValidationError as e:
                        if attempt < max_retries - 1:
                            if callback:
                                callback(f"Validation failed: {str(e)}. Retrying...", step_name)
                            continue
                        raise

                else:
                    error = (
                        f"Invalid response structure: Expected object with keys {list(expected_outputs.keys())}, "
                        f"got {type(parsed_output).__name__}"
                    )
                    attempts_history.append((error, cleaned_content))
                    if attempt < max_retries - 1:
                        if callback:
                            callback(f"Validation failed: {error}. Retrying...", step_name)
                        continue
                    raise OutputValidationError(error)

            except Exception as e:
                error = str(e)
                if attempt < max_retries - 1:
                    if callback:
                        callback(f"Attempt {attempt + 1} failed: {error}. Retrying...", step_name)
                    continue
                raise e

        raise OutputValidationError(f"Failed after {max_retries} attempts. Last error: {error}")

    def log_error(self, prompt: str, response: str, error: Exception):
        """
        Logs the prompt, response, and error to assist in debugging.
        Suggests potential improvements to the YAML prompt.
        """
        print("[ERROR] Failed to parse response.")
        print("[PROMPT]:", prompt)
        print("[RAW RESPONSE]:", response)
        print("[ERROR DETAILS]:", error)
        print("[SUGGESTION]: Review the YAML prompt. Ensure it guides the LLM to produce strictly JSON-formatted output.")

    def add_prompt_schema(self, prompt: str, expected_outputs: Dict[str, Any]) -> str:
        return f"{prompt}\n\nOnly answer with the following JSON schema:\n{json.dumps(expected_outputs)}\nDo not generate any other text."

    def run(
        self, 
        steps_file: str, 
        initial_inputs: Dict[str, Any], 
        callback: Optional[Callable[[str, Optional[str]], None]] = None
    ) -> Dict[str, Any]:
        self.context.update(initial_inputs)
        execution_log = {
            "initial_inputs": initial_inputs,
            "steps": [],
            "final_result": {}
        }

        # Load YAML steps
        steps = self.load_steps(steps_file, initial_inputs)

        for step_name, step in steps.items():
            step_log = {
                step_name: {
                    "input": {},
                    "output": None,
                    "schema": step.outputs,
                    "errors": []
                }
            }
            try:
                # Validate required inputs
                for input_key in step.inputs.keys():
                    if input_key not in self.context or self.context[input_key] is None:
                        raise ValueError(f"Missing or invalid input '{input_key}' for step '{step_name}'.")
                    step_log[step_name]["input"][input_key] = self.context[input_key]

                prompt = self.format_task(step.task, self.context)
                prompt = self.add_prompt_schema(prompt, step.outputs)

                if callback:
                    callback(f"Executing step with task: {prompt}", step_name)

                result = self.query_llm(
                    prompt=prompt,
                    expected_outputs=step.outputs,
                    max_retries=step.max_retries,
                    callback=lambda msg, step_name=step_name: callback(msg, step_name) if callback else None,
                    step_name=step_name
                )

                # Map response to context based on YAML outputs
                for output_name, output_schema in step.outputs.items():
                    # Store the actual value, not the wrapped response
                    if len(step.outputs) == 1:
                        self.context[output_name] = result[output_name]
                    else:
                        self.context[output_name] = result.get(output_name)
                step_log[step_name]["output"] = result

                if callback:
                    callback(f"Step '{step_name}' completed successfully.")
            except Exception as e:
                print(f"[ERROR] Step '{step_name}' failed: {e}")
                error_detail = {
                    'error': str(e),
                    'timestamp': datetime.now().isoformat(),
                    'context': {
                        'prompt': step.task,
                        'expected_schema': step.outputs
                    }
                }
                step_log[step_name]['errors'].append(error_detail)
                if callback:
                    callback(f"Step '{step_name}' failed: {str(e)}")
                    callback(f"Skipping step '{step_name}' due to error.")
                # Use default value `None` for all defined outputs of the step
                for output_name in step.outputs.keys():
                    self.context[output_name] = None
                step_log[step_name]["output"] = None

            execution_log["steps"].append(step_log)

        # Only include the last step's output in the final result
        if execution_log["steps"]:
            last_step = execution_log["steps"][-1]
            last_step_name = list(last_step.keys())[0]
            last_output = last_step[last_step_name]["output"]
            if last_output:
                execution_log["final_result"] = last_output

        execution_log["error_count"] = sum(1 for step in execution_log["steps"] if step[list(step.keys())[0]]["errors"] is not None)
        return execution_log

if __name__ == "__main__":
    from dotenv import load_dotenv
    from rich import print
    import argparse

    load_dotenv(override=True)

    parser = argparse.ArgumentParser()
    parser.add_argument("--steps_file", type=str, default="steps.yaml")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--inputs", type=json.loads, default={})
    parser.add_argument("--llm_base_url", type=str, default=os.getenv("OPENAI_API_BASE"))
    parser.add_argument("--llm_api_key", type=str, default=os.getenv("OPENAI_API_KEY"))
    parser.add_argument("--llm_model_name", type=str, default=os.getenv("OPENAI_MODEL_NAME"))
    args = parser.parse_args()

    def callback(message: str, step_name: Optional[str] = None):
        print(f"[INFO] {message}")

    ai_stepper = AI_Stepper(
        llm_base_url=args.llm_base_url,
        llm_api_key=args.llm_api_key,
        llm_model_name=args.llm_model_name,
    )

    # easy
    # python .\ai_stepper.py --steps_file .\yaml\easy.yaml --inputs '{\"user_request\": \"6+18\"}'

    # medium
    # python .\ai_stepper.py --steps_file .\yaml\medium.yaml --inputs '{\"count\": 10, \"min_value\": 1, \"max_value\": 100}'

    # hard
    # python .\ai_stepper.py --steps_file .\yaml\hard.yaml --inputs '{\"count\": 10}'

    initial_inputs = args.inputs
    if not isinstance(initial_inputs, dict):
        raise Exception("initial_inputs must be a dictionary")

    print("[INITIAL INPUTS]", initial_inputs)    

    final_context = ai_stepper.run(
        steps_file=args.steps_file,
        initial_inputs=initial_inputs, 
        callback=callback
    )
    print("[RESULT]", final_context)
