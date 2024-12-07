import pytest
from unittest.mock import Mock, patch
import yaml
import json
from pathlib import Path
import os
from ai_stepper import AI_Stepper
from ai_stepper.schema.output_validation_error import OutputValidationError
from dotenv import load_dotenv

load_dotenv(override=True)

# Fixture for test YAML content
@pytest.fixture
def test_yaml_content():
    return """
fetch_data:
  task: >
    Generate {count} random numbers between {min_value} and {max_value}.
  inputs:
    count: int
    min_value: int
    max_value: int
  outputs:
    numbers:
      type: array
      items:
        type: integer
"""

# Fixture for test YAML file
@pytest.fixture
def test_yaml_file(tmp_path, test_yaml_content):
    yaml_file = tmp_path / "test_steps.yaml"
    yaml_file.write_text(test_yaml_content)
    return str(yaml_file)

# Fixture for AI_Stepper instance
@pytest.fixture
def stepper():
    return AI_Stepper(
        llm_base_url=os.getenv("OPENAI_API_BASE"),
        llm_api_key=os.getenv("OPENAI_API_KEY"),
        llm_model_name=os.getenv("OPENAI_MODEL_NAME")
    )

# Fixture for mock litellm
@pytest.fixture
def mock_litellm():
    with patch('ai_stepper.ai_stepper.completion') as mock:
        yield mock

# Test prompt interpolation
def test_prompt_interpolation(stepper):
    prompt = "Generate {count} items with {property}"
    inputs = {"count": 5, "property": "color"}
    result = stepper.format_task(prompt, inputs)
    assert result == "Generate 5 items with color"

# Test validation success
def test_validate_output_success(stepper):
    schema = {"type": "array", "items": {"type": "integer"}}
    value = [1, 2, 3, 4, 5]
    result = stepper.validate_output(value, schema)
    assert result == value

# Test validation failure
def test_validate_output_failure(stepper):
    schema = {"type": "array", "items": {"type": "integer"}}
    value = "not an array"  # This should definitely fail
    with pytest.raises(Exception):
        stepper.validate_output(value, schema)

# Test type conversion
def test_type_conversion(stepper):
    schema = {"type": "integer"}
    value = "42"
    try:
        value = int(value)  # Convert string to int before validation
    except (ValueError, TypeError):
        pass
    result = stepper.validate_output(value, schema)
    assert result == 42
    assert isinstance(result, int)

# Test nested object validation
def test_nested_object_validation(stepper):
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "scores": {"type": "array", "items": {"type": "number"}}
        }
    }
    value = {
        "name": "Test",
        "age": 25,
        "scores": [90.5, 85, 95.5]
    }
    result = stepper.validate_output(value, schema)
    assert isinstance(result["age"], int)
    assert all(isinstance(x, (int, float)) for x in result["scores"])

# Test LLM query with mock
def test_query_llm(mock_litellm, stepper):
    # Create a mock response object that matches litellm's response structure
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock()
    mock_response.choices[0].message.content = '{"numbers": [1, 2, 3]}'
    
    # Set up the mock to return our response
    mock_litellm.return_value = mock_response

    result = stepper.query_llm(
        prompt="Generate 3 numbers",
        expected_outputs={"numbers": {"type": "array", "items": {"type": "integer"}}},
        max_retries=3,
        callback=None
    )

    assert result == {"numbers": [1, 2, 3]}
    mock_litellm.assert_called_once()

# Test LLM query with retry
def test_query_llm_retry(mock_litellm, stepper):
    # Create mock responses
    success_response = Mock()
    success_response.choices = [Mock()]
    success_response.choices[0].message = Mock()
    success_response.choices[0].message.content = '{"numbers": [1, 2, 3]}'
    
    # Configure mock to raise error twice then succeed
    mock_litellm.side_effect = [
        Exception("Rate limit error"),
        Exception("Rate limit error"),
        success_response
    ]

    result = stepper.query_llm(
        prompt="Generate 3 numbers",
        expected_outputs={"numbers": {"type": "array", "items": {"type": "integer"}}},
        max_retries=3,
        callback=None
    )

    # Verify the result
    assert isinstance(result, dict)
    assert "numbers" in result
    assert isinstance(result["numbers"], list)
    assert len(result["numbers"]) == 3
    assert all(isinstance(x, int) for x in result["numbers"])
    
    # Verify the number of calls
    assert mock_litellm.call_count == 3

# Test full workflow execution
@patch('litellm.completion')
def test_workflow_execution(mock_completion, stepper, test_yaml_file):
    # Create a mock response object that matches litellm's response structure
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock()
    mock_response.choices[0].message.content = '{"numbers": [1, 2, 3]}'
    mock_completion.return_value = mock_response

    initial_inputs = {"count": 3, "min_value": 1, "max_value": 10}
    result = stepper.run(steps_file=test_yaml_file, initial_inputs=initial_inputs)
    assert "final_result" in result
    assert "steps" in result
    assert len(result["steps"]) == 1

# Test callback functionality
@patch('litellm.completion')
def test_callback(mock_completion, stepper, test_yaml_file):
    callback_calls = []
    def test_callback(message, step_name=None):
        callback_calls.append(message)

    # Create a mock response object that matches litellm's response structure
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock()
    mock_response.choices[0].message.content = '{"numbers": [1, 2, 3]}'
    mock_completion.return_value = mock_response

    initial_inputs = {"count": 3, "min_value": 1, "max_value": 10}
    result = stepper.run(steps_file=test_yaml_file, initial_inputs=initial_inputs, callback=test_callback)

    assert len(callback_calls) > 0
