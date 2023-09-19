import pytest
import tempfile
import yaml
import json
from pathlib import Path
from click.testing import CliRunner
from yaml2dot.__main__ import render_yaml

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

def test_render_yaml(temp_dir, capfd):
    yaml_data = [
        {'Key': 'key1', 'Value': 'value1'},
        {'Key': 'key2', 'Value': {'nested_key': 'nested_value'}},
        {'Key': 'key3', 'Value': [1, 2, 3]},
    ]

    yaml_file = temp_dir / "test.yaml"
    dot_file = temp_dir / "test.dot"

    with open(yaml_file, "w") as f:
        yaml.dump(yaml_data, f)

    runner = CliRunner()
    result = runner.invoke(render_yaml, [f"--input-file={yaml_file}", f"--output-file={dot_file}", "--rankdir=LR"])

    assert dot_file.exists()

    # Capture the printed output and assert on it
    captured = capfd.readouterr()
    assert "Error" not in captured.err  # Make sure there are no error messages

def test_render_yaml_invalid_input(temp_dir):
    # Create an invalid YAML file
    yaml_file = temp_dir / "invalid.yaml"
    with open(yaml_file, "w") as f:
        f.write("key1: value1\nkey2: value2\nkey3: value3:")

    runner = CliRunner()
    result = runner.invoke(render_yaml, [f"--input-file={yaml_file}", f"--output-file={temp_dir / 'test.dot'}", "--rankdir=LR"],standalone_mode=False)
    print(result.return_value)
    # Check if the result contains the expected error message
    assert "Error" in result.output
    assert not (temp_dir / "test.dot").exists()

def test_render_json(temp_dir):
    json_data = {
        "key1": "value1",
        "key2": {
            "nested_key": "nested_value"
        },
        "key3": [1, 2, 3]
    }

    json_file = temp_dir / "test_json.json"
    dot_file = temp_dir / "test_json.dot"

    with open(json_file, "w") as f:
        json.dump(json_data, f)
        
    runner = CliRunner()
    result = runner.invoke(render_yaml, [f"--input-file={json_file}", f"--output-file={dot_file}", "--rankdir=LR"])
    assert dot_file.exists()

    # Check if the generated DOT file is valid
    with open(dot_file, "r") as f:
        dot_contents = f.read()
        assert "digraph" in dot_contents 

def test_render_json_invalid_input(temp_dir):
    # Create an invalid JSON file
    json_file = temp_dir / "invalid.json"
    with open(json_file, "w") as f:
        f.write("key1: value1, key2: value2")

    runner = CliRunner()
    result = runner.invoke(render_yaml, [f"--input-file={json_file}", "--output-file=test_json.dot", "--rankdir=LR"])
    # Check if the result contains the expected error message
    assert "Error" in result.output
    assert not (temp_dir / "test.dot").exists()
    
def test_render_json_output(temp_dir):
    json_data = {
        "key1": "value1",
        "key2": {
            "nested_key": "nested_value"
        },
        "key3": [1, 2, 3]
    }

    json_file = temp_dir / "test_json.json"
    dot_file = temp_dir / "test_json.dot"

    with open(json_file, "w") as f:
        json.dump(json_data, f)
        
    runner = CliRunner()
    result = runner.invoke(render_yaml, [f"--input-file={json_file}", f"--output-file={dot_file}", "--rankdir=LR", "--output-format=json"])
    assert dot_file.exists()
    # Check if the generated JSON file is valid
    with open(dot_file, "r") as f:
        json_contents = json.load(f)
        print(json_contents)
        assert "nodes" in json_contents  # Ensure JSON data is preserved

def test_render_json_output_invalid_input(temp_dir):
    # Create an invalid JSON file
    json_file = temp_dir / "invalid.json"
    with open(json_file, "w") as f:
        f.write("key1: value1, key2: value2")

    runner = CliRunner()
    result = runner.invoke(render_yaml, [f"--input-file={json_file}", "--output-file=test_json.dot", "--rankdir=LR", "--output-format=json"])
    # Check if the result contains the expected error message
    assert "Error" in result.output
    assert not (temp_dir / "test_json.dot").exists()