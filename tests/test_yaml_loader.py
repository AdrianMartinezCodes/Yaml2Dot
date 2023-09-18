import io

import pytest
import yaml

from yaml2dot.yaml_loader import parse_yaml


@pytest.fixture
def sample_yaml_content():
    return """\
        key1: value1
        key2: value2
    """


def test_parse_yaml(sample_yaml_content):
    reader = io.StringIO(sample_yaml_content)
    parsed_data, error = parse_yaml(reader)

    assert error is None
    expected = {'key1': 'value1', 'key2': 'value2'}
    assert parsed_data == expected


def test_parse_yaml_with_error():
    # Simulate a YAML parsing error
    invalid_yaml = "key1: value1\nkey2: value2\nkey3: value3:"  # Invalid YAML
    reader = io.StringIO(invalid_yaml)
    parsed_data, error = parse_yaml(reader)

    assert parsed_data is None
    assert isinstance(error, yaml.YAMLError)
