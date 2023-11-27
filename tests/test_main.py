import json
import tempfile
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from yaml2dot.__main__ import render_yaml


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


def test_render_yaml(temp_dir, capfd):
    yaml_data = [
        {
            'Key': 'key1',
            'Value': 'value1'
        },
        {
            'Key': 'key2',
            'Value': {
                'nested_key': 'nested_value'
            }
        },
        {
            'Key': 'key3',
            'Value': [1, 2, 3]
        },
    ]

    yaml_file = temp_dir / "test.yaml"
    dot_file = temp_dir / "test.dot"

    with open(yaml_file, "w") as f:
        yaml.dump(yaml_data, f)

    runner = CliRunner()
    result = runner.invoke(render_yaml, [
        f"--input-file={yaml_file}", f"--output-file={dot_file}", "--rankdir=LR"
    ])

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
    result = runner.invoke(render_yaml, [
        f"--input-file={yaml_file}", f"--output-file={temp_dir / 'test.dot'}",
        "--rankdir=LR"
    ],
                           standalone_mode=False)
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
    result = runner.invoke(render_yaml, [
        f"--input-file={json_file}", f"--output-file={dot_file}", "--rankdir=LR"
    ])
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
    result = runner.invoke(render_yaml, [
        f"--input-file={json_file}", "--output-file=test_json.dot",
        "--rankdir=LR"
    ])
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
    result = runner.invoke(render_yaml, [
        f"--input-file={json_file}", f"--output-file={dot_file}",
        "--rankdir=LR", "--output-format=json"
    ])
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
    result = runner.invoke(render_yaml, [
        f"--input-file={json_file}", "--output-file=test_json.dot",
        "--rankdir=LR", "--output-format=json"
    ])
    # Check if the result contains the expected error message
    assert "Error" in result.output
    assert not (temp_dir / "test_json.dot").exists()


def test_render_yaml_stream(temp_dir, capfd):
    yaml_data = [
        {
            'Key': 'key1',
            'Value': 'value1'
        },
        {
            'Key': 'key2',
            'Value': {
                'nested_key': 'nested_value'
            }
        },
        {
            'Key': 'key3',
            'Value': [1, 2, 3]
        },
    ]

    yaml_file = temp_dir / "test.yaml"

    with open(yaml_file, "w") as f:
        json.dump(yaml_data, f)

    runner = CliRunner()

    # Test rendering to JSON format and capturing stdout
    result = runner.invoke(render_yaml, [
        f"--input-file={yaml_file}", "--output-file=-", "--output-format=json",
        "--rankdir=LR"
    ])

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
    expected_nodes = [{
        "label": "Value",
        "fontname": "Fira Mono",
        "fontsize": "10",
        "margin": "0.3,0.1",
        "fillcolor": "#fafafa",
        "penwidth": 2.0,
        "style": "rounded",
        "shape": "rounded",
        "id": "0__Value"
    }, {
        "label": "0",
        "id": "0"
    }, {
        "label": "Key",
        "fontname": "Fira Mono",
        "fontsize": "10",
        "margin": "0.3,0.1",
        "fillcolor": "#fafafa",
        "penwidth": 2.0,
        "style": "rounded",
        "shape": "rounded",
        "id": "0__Key"
    }, {
        "label": "key3",
        "fontname": "Fira Mono",
        "fontsize": "10",
        "margin": "0.3,0.1",
        "fillcolor": "#fafafa",
        "penwidth": 2.0,
        "style": "rounded",
        "shape": "rounded",
        "id": "0__Key__key3"
    }, {
        "label": "key2",
        "fontname": "Fira Mono",
        "fontsize": "10",
        "margin": "0.3,0.1",
        "fillcolor": "#fafafa",
        "penwidth": 2.0,
        "style": "rounded",
        "shape": "rounded",
        "id": "0__Key__key2"
    }, {
        "label": "key1",
        "fontname": "Fira Mono",
        "fontsize": "10",
        "margin": "0.3,0.1",
        "fillcolor": "#fafafa",
        "penwidth": 2.0,
        "style": "rounded",
        "shape": "rounded",
        "id": "0__Key__key1"
    }, {
        "label": "value1",
        "fontname": "Fira Mono",
        "fontsize": "10",
        "margin": "0.3,0.1",
        "fillcolor": "#fafafa",
        "penwidth": 2.0,
        "style": "rounded",
        "shape": "rounded",
        "id": "0__Value__value1"
    }, {
        "label": "3",
        "fontname": "Fira Mono",
        "fontsize": "10",
        "margin": "0.3,0.1",
        "fillcolor": "#fafafa",
        "penwidth": 2.0,
        "style": "rounded",
        "shape": "rounded",
        "id": "0__Value__3"
    }, {
        "label": "2",
        "fontname": "Fira Mono",
        "fontsize": "10",
        "margin": "0.3,0.1",
        "fillcolor": "#fafafa",
        "penwidth": 2.0,
        "style": "rounded",
        "shape": "rounded",
        "id": "0__Value__2"
    }, {
        "label": "1",
        "fontname": "Fira Mono",
        "fontsize": "10",
        "margin": "0.3,0.1",
        "fillcolor": "#fafafa",
        "penwidth": 2.0,
        "style": "rounded",
        "shape": "rounded",
        "id": "0__Value__1"
    }, {
        "label": "nested_key",
        "fontname": "Fira Mono",
        "fontsize": "10",
        "margin": "0.3,0.1",
        "fillcolor": "#fafafa",
        "penwidth": 2.0,
        "style": "rounded",
        "shape": "rounded",
        "id": "0__Value__nested_key"
    }, {
        "label": "nested_value",
        "fontname": "Fira Mono",
        "fontsize": "10",
        "margin": "0.3,0.1",
        "fillcolor": "#fafafa",
        "penwidth": 2.0,
        "style": "rounded",
        "shape": "rounded",
        "id": "0__Value__nested_key__nested_value"
    }]
    expected_links = [{
        "arrowhead": "none",
        "penwidth": "2.0",
        "source": "0__Value",
        "target": "0__Value__value1",
        "key": 0
    }, {
        "arrowhead": "none",
        "penwidth": "2.0",
        "source": "0__Value",
        "target": "0__Value__3",
        "key": 0
    }, {
        "arrowhead": "none",
        "penwidth": "2.0",
        "source": "0__Value",
        "target": "0__Value__2",
        "key": 0
    }, {
        "arrowhead": "none",
        "penwidth": "2.0",
        "source": "0__Value",
        "target": "0__Value__1",
        "key": 0
    }, {
        "arrowhead": "none",
        "penwidth": "2.0",
        "source": "0__Value",
        "target": "0__Value__nested_key",
        "key": 0
    }, {
        "arrowhead": "none",
        "penwidth": "2.0",
        "source": "0",
        "target": "0__Value",
        "key": 0
    }, {
        "arrowhead": "none",
        "penwidth": "2.0",
        "source": "0",
        "target": "0__Key",
        "key": 0
    }, {
        "arrowhead": "none",
        "penwidth": "2.0",
        "source": "0__Key",
        "target": "0__Key__key3",
        "key": 0
    }, {
        "arrowhead": "none",
        "penwidth": "2.0",
        "source": "0__Key",
        "target": "0__Key__key2",
        "key": 0
    }, {
        "arrowhead": "none",
        "penwidth": "2.0",
        "source": "0__Key",
        "target": "0__Key__key1",
        "key": 0
    }, {
        "arrowhead": "none",
        "penwidth": "2.0",
        "source": "0__Value__nested_key",
        "target": "0__Value__nested_key__nested_value",
        "key": 0
    }]
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
    result = runner.invoke(render_yaml, [
        f"--input-file={yaml_file}", f"--output-file=-", "--rankdir=LR",
        "--output-format=json"
    ],
                           standalone_mode=False)

    # Check if the result contains the expected error message
    assert "Error" in result.output
    assert not (temp_dir / "test.json").exists()


def test_render_yaml_with_round_robin(temp_dir):
    # Setup code for input YAML
    yaml_data = {
        "key1": "value1",
        "key2": {
            "nested_key": "nested_value"
        },
        "key3": [1, 2, 3]
    }
    yaml_file = temp_dir / "test.yaml"
    dot_file = temp_dir / "test_round_robin.dot"
    with open(yaml_file, "w") as f:
        yaml.dump(yaml_data, f)

    runner = CliRunner()
    result = runner.invoke(render_yaml, [
        "--input-file",
        str(yaml_file), "--output-file",
        str(dot_file), "--rankdir", "LR", "--round-robin"
    ])

    assert dot_file.exists()
    with open(dot_file, "r") as f:
        dot_contents = f.read()
        assert "rounded" in dot_contents or "box" in dot_contents


def test_render_yaml_with_shape(temp_dir):
    # Setup code for input YAML
    yaml_data = {
        "key1": "value1",
        "key2": {
            "nested_key": "nested_value"
        },
        "key3": [1, 2, 3]
    }
    yaml_file = temp_dir / "test.yaml"
    dot_file = temp_dir / "test_shape.dot"
    shape = "box"

    with open(yaml_file, "w") as f:
        yaml.dump(yaml_data, f)

    runner = CliRunner()
    result = runner.invoke(render_yaml, [
        "--input-file",
        str(yaml_file), "--output-file",
        str(dot_file), "--rankdir", "LR", "--shape", shape
    ])

    assert dot_file.exists()
    with open(dot_file, "r") as f:
        dot_contents = f.read()
        assert shape in dot_contents
