import io
import json
import os
import tempfile

import pytest
import yaml

from yaml2dot.data_loader import load_yaml_or_json, parse_yaml


@pytest.fixture
def sample_yaml_content():
    return """\
        key1: value1
        key2: value2
    """


@pytest.fixture
def invalid_yaml_content():
    return "key1: value1\nkey2: value2\nkey3: value3:"  # Invalid YAML


def test_parse_yaml(sample_yaml_content):
    reader = io.StringIO(sample_yaml_content)
    parsed_data, error = parse_yaml(reader)

    assert error is None
    expected = [{'key1': 'value1', 'key2': 'value2'}]
    assert parsed_data == expected


def test_parse_yaml_with_error(invalid_yaml_content):
    # Simulate a YAML parsing error
    reader = io.StringIO(invalid_yaml_content)
    parsed_data, error = parse_yaml(reader)

    assert parsed_data is None
    assert isinstance(error, yaml.YAMLError)


def test_parse_yaml_empty_input():
    # Simulate an empty YAML input
    reader = io.StringIO("")
    parsed_data, error = parse_yaml(reader)

    assert not parsed_data  # Empty yaml is None
    assert error is None


@pytest.fixture
def temp_yaml_file():
    # Create a temporary YAML file with sample content
    content = """\
        key1: value1
        key2: value2
    """
    with tempfile.NamedTemporaryFile(delete=False, mode='w',
                                     suffix=".yaml") as file:
        file.write(content)
        file_path = file.name
    yield file_path
    os.remove(file_path)


@pytest.fixture
def temp_json_file():
    # Create a temporary JSON file with sample content
    content = '{"key1": "value1", "key2": "value2"}'
    with tempfile.NamedTemporaryFile(delete=False, mode='w',
                                     suffix=".json") as file:
        file.write(content)
        file_path = file.name
    yield file_path
    os.remove(file_path)


def test_load_yaml_or_json_valid_json(temp_json_file):
    data = load_yaml_or_json(temp_json_file)
    expected = {'key1': 'value1', 'key2': 'value2'}
    assert data == expected


def test_load_yaml_or_json_invalid_yaml():
    # Simulate loading an invalid YAML file
    invalid_yaml = "key1: value1\nkey2: value2\nkey3: value3:"  # Invalid YAML
    with tempfile.NamedTemporaryFile(delete=False, mode='w',
                                     suffix=".yaml") as file:
        file.write(invalid_yaml)
        temp_yaml_file = file.name

    data = load_yaml_or_json(temp_yaml_file)
    assert data is None


def test_load_yaml_or_json_invalid_json():
    # Simulate loading an invalid JSON file
    invalid_json = '{"key1": "value1", "key2": "value2", "key3": "value3":}'  # Invalid JSON
    with tempfile.NamedTemporaryFile(delete=False, mode='w',
                                     suffix=".json") as file:
        file.write(invalid_json)
        temp_json_file = file.name

    data = load_yaml_or_json(temp_json_file)
    assert data is None


def test_load_yaml_or_json_invalid_file_extension():
    # Simulate loading a file with an unsupported extension
    invalid_file = tempfile.NamedTemporaryFile(delete=False,
                                               mode='w',
                                               suffix=".txt")
    invalid_file_path = invalid_file.name
    invalid_file.close()

    data = load_yaml_or_json(invalid_file_path)
    assert data is None
    os.remove(invalid_file_path)
