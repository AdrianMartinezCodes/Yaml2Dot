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
        assert "nodes" in json_contents

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
    
    
def test_render_yaml_stream(temp_dir, capfd):
    yaml_data = [
        {'Key': 'key1', 'Value': 'value1'},
        {'Key': 'key2', 'Value': {'nested_key': 'nested_value'}},
        {'Key': 'key3', 'Value': [1, 2, 3]},
    ]

    yaml_file = temp_dir / "test.yaml"

    with open(yaml_file, "w") as f:
        json.dump(yaml_data, f) 

    runner = CliRunner()
    
    # Test rendering to JSON format and capturing stdout
    result = runner.invoke(render_yaml, [f"--input-file={yaml_file}", "--output-file=-", "--output-format=json", "--rankdir=LR"])
    
    # Capture the printed JSON output and assert on it
    captured = capfd.readouterr()
    parsed_json = json.loads(result.output)
    
    # Check the JSON structure and data
    assert isinstance(parsed_json, dict)
    assert "nodes" in parsed_json
    assert "links" in parsed_json
    assert "directed" in parsed_json
    assert parsed_json["directed"] is True 
    
    
    # Check that the JSON contains the expected data from the YAML input
    expected_nodes = [
    {
      "label": "Key",
      "fontname": "Fira Mono",
      "fontsize": "10",
      "margin": "0.3,0.1",
      "fillcolor": "#fafafa",
      "shape": "box",
      "penwidth": 2.0,
      "style": "rounded",
      "id": "None/0/None/Key"
    },
    {
      "label": "None",
      "id": "None/0/None"
    },
    {
      "label": "key1",
      "fontname": "Fira Mono",
      "fontsize": "10",
      "margin": "0.3,0.1",
      "fillcolor": "#fafafa",
      "shape": "box",
      "penwidth": 2.0,
      "style": "rounded",
      "id": "None/0/None/Key/key1"
    },
    {
      "label": "Value",
      "fontname": "Fira Mono",
      "fontsize": "10",
      "margin": "0.3,0.1",
      "fillcolor": "#fafafa",
      "shape": "box",
      "penwidth": 2.0,
      "style": "rounded",
      "id": "None/0/None/Value"
    },
    {
      "label": "value1",
      "fontname": "Fira Mono",
      "fontsize": "10",
      "margin": "0.3,0.1",
      "fillcolor": "#fafafa",
      "shape": "box",
      "penwidth": 2.0,
      "style": "rounded",
      "id": "None/0/None/Value/value1"
    },
    {
      "label": "Key",
      "fontname": "Fira Mono",
      "fontsize": "10",
      "margin": "0.3,0.1",
      "fillcolor": "#fafafa",
      "shape": "box",
      "penwidth": 2.0,
      "style": "rounded",
      "id": "None/1/None/Key"
    },
    {
      "label": "None",
      "id": "None/1/None"
    },
    {
      "label": "key2",
      "fontname": "Fira Mono",
      "fontsize": "10",
      "margin": "0.3,0.1",
      "fillcolor": "#fafafa",
      "shape": "box",
      "penwidth": 2.0,
      "style": "rounded",
      "id": "None/1/None/Key/key2"
    },
    {
      "label": "Value",
      "fontname": "Fira Mono",
      "fontsize": "10",
      "margin": "0.3,0.1",
      "fillcolor": "#fafafa",
      "shape": "box",
      "penwidth": 2.0,
      "style": "rounded",
      "id": "None/1/None/Value"
    },
    {
      "label": "nested_key",
      "fontname": "Fira Mono",
      "fontsize": "10",
      "margin": "0.3,0.1",
      "fillcolor": "#fafafa",
      "shape": "box",
      "penwidth": 2.0,
      "style": "rounded",
      "id": "None/1/None/Value/nested_key"
    },
    {
      "label": "nested_value",
      "fontname": "Fira Mono",
      "fontsize": "10",
      "margin": "0.3,0.1",
      "fillcolor": "#fafafa",
      "shape": "box",
      "penwidth": 2.0,
      "style": "rounded",
      "id": "None/1/None/Value/nested_key/nested_value"
    },
    {
      "label": "Key",
      "fontname": "Fira Mono",
      "fontsize": "10",
      "margin": "0.3,0.1",
      "fillcolor": "#fafafa",
      "shape": "box",
      "penwidth": 2.0,
      "style": "rounded",
      "id": "None/2/None/Key"
    },
    {
      "label": "None",
      "id": "None/2/None"
    },
    {
      "label": "key3",
      "fontname": "Fira Mono",
      "fontsize": "10",
      "margin": "0.3,0.1",
      "fillcolor": "#fafafa",
      "shape": "box",
      "penwidth": 2.0,
      "style": "rounded",
      "id": "None/2/None/Key/key3"
    },
    {
      "label": "Value",
      "fontname": "Fira Mono",
      "fontsize": "10",
      "margin": "0.3,0.1",
      "fillcolor": "#fafafa",
      "shape": "box",
      "penwidth": 2.0,
      "style": "rounded",
      "id": "None/2/None/Value"
    },
    {
      "label": "1",
      "fontname": "Fira Mono",
      "fontsize": "10",
      "margin": "0.3,0.1",
      "fillcolor": "#fafafa",
      "shape": "box",
      "penwidth": 2.0,
      "style": "rounded",
      "id": "1"
    },
    {
      "label": "Value",
      "id": "None/2/None/Value/0/None/2/None/Value"
    },
    {
      "label": "2",
      "fontname": "Fira Mono",
      "fontsize": "10",
      "margin": "0.3,0.1",
      "fillcolor": "#fafafa",
      "shape": "box",
      "penwidth": 2.0,
      "style": "rounded",
      "id": "2"
    },
    {
      "label": "Value",
      "id": "None/2/None/Value/1/None/2/None/Value"
    },
    {
      "label": "3",
      "fontname": "Fira Mono",
      "fontsize": "10",
      "margin": "0.3,0.1",
      "fillcolor": "#fafafa",
      "shape": "box",
      "penwidth": 2.0,
      "style": "rounded",
      "id": "3"
    },
    {
      "label": "Value",
      "id": "None/2/None/Value/2/None/2/None/Value"
    }
  ]
    expected_links = [
    {
      "arrowhead": "none",
      "penwidth": "2.0",
      "source": "None/0/None/Key",
      "target": "None/0/None/Key/key1",
      "key": 0
    },
    {
      "arrowhead": "none",
      "penwidth": "2.0",
      "source": "None/0/None",
      "target": "None/0/None/Key",
      "key": 0
    },
    {
      "arrowhead": "none",
      "penwidth": "2.0",
      "source": "None/0/None",
      "target": "None/0/None/Value",
      "key": 0
    },
    {
      "arrowhead": "none",
      "penwidth": "2.0",
      "source": "None/0/None/Value",
      "target": "None/0/None/Value/value1",
      "key": 0
    },
    {
      "arrowhead": "none",
      "penwidth": "2.0",
      "source": "None/1/None/Key",
      "target": "None/1/None/Key/key2",
      "key": 0
    },
    {
      "arrowhead": "none",
      "penwidth": "2.0",
      "source": "None/1/None",
      "target": "None/1/None/Key",
      "key": 0
    },
    {
      "arrowhead": "none",
      "penwidth": "2.0",
      "source": "None/1/None",
      "target": "None/1/None/Value",
      "key": 0
    },
    {
      "arrowhead": "none",
      "penwidth": "2.0",
      "source": "None/1/None/Value",
      "target": "None/1/None/Value/nested_key",
      "key": 0
    },
    {
      "arrowhead": "none",
      "penwidth": "2.0",
      "source": "None/1/None/Value/nested_key",
      "target": "None/1/None/Value/nested_key/nested_value",
      "key": 0
    },
    {
      "arrowhead": "none",
      "penwidth": "2.0",
      "source": "None/2/None/Key",
      "target": "None/2/None/Key/key3",
      "key": 0
    },
    {
      "arrowhead": "none",
      "penwidth": "2.0",
      "source": "None/2/None",
      "target": "None/2/None/Key",
      "key": 0
    },
    {
      "arrowhead": "none",
      "penwidth": "2.0",
      "source": "None/2/None",
      "target": "None/2/None/Value",
      "key": 0
    },
    {
      "arrowhead": "none",
      "penwidth": "2.0",
      "source": "None/2/None/Value/0/None/2/None/Value",
      "target": "1",
      "key": 0
    },
    {
      "arrowhead": "none",
      "penwidth": "2.0",
      "source": "None/2/None/Value/1/None/2/None/Value",
      "target": "2",
      "key": 0
    },
    {
      "arrowhead": "none",
      "penwidth": "2.0",
      "source": "None/2/None/Value/2/None/2/None/Value",
      "target": "3",
      "key": 0
    }
  ]
    # Check that the JSON contains the expected nodes and links
    for node in expected_nodes:
        assert node in parsed_json["nodes"]

    for link in expected_links:
        assert link in parsed_json["links"]

    assert not (temp_dir / "test.json").exists()

def test_render_yaml_stream_invalid_input(temp_dir):
    # Create an invalid YAML file
    yaml_file = temp_dir / "invalid.yaml"
    with open(yaml_file, "w") as f:
        f.write("key1: value1\nkey2: value2\nkey3: value3:")

    runner = CliRunner()
    result = runner.invoke(render_yaml, [f"--input-file={yaml_file}", f"--output-file=-", "--rankdir=LR", "--output-format=json"],standalone_mode=False)
    
    # Check if the result contains the expected error message
    assert "Error" in result.output
    assert not (temp_dir / "test.json").exists()