import json

import networkx as nx
import pytest

from yaml2dot.converter import convert_yaml_or_json_to_format

# Define sample YAML and JSON data for testing
sample_yaml_data = {
    'key1': 'value1',
    'key2': {
        'nested_key': 'nested_value'
    },
    'key3': [1, 2, 3]
}

sample_json_data = {
    'nodes': [{
        'id': 'A',
        'label': 'Node A'
    }, {
        'id': 'B',
        'label': 'Node B'
    }],
    'links': [{
        'source': 'A',
        'target': 'B'
    }, {
        'source': 'B',
        'target': 'A'
    }]
}


def test_convert_yaml_to_dot():
    dot_output = convert_yaml_or_json_to_format(sample_yaml_data,
                                                output_format='dot')
    assert dot_output is not None
    assert isinstance(dot_output, str)
    # You can add further assertions based on the expected DOT output.


def test_convert_yaml_to_json():
    json_output = convert_yaml_or_json_to_format(sample_yaml_data,
                                                 output_format='json')
    assert json_output is not None
    assert isinstance(json_output, str)
    # You can add further assertions based on the expected JSON output.


def test_convert_json_to_dot():
    dot_output = convert_yaml_or_json_to_format(sample_json_data,
                                                output_format='dot')
    assert dot_output is not None
    assert isinstance(dot_output, str)
    # You can add further assertions based on the expected DOT output.


def test_convert_json_to_json():
    json_output = convert_yaml_or_json_to_format(sample_json_data,
                                                 output_format='json')
    assert json_output is not None
    assert isinstance(json_output, str)
    # You can add further assertions based on the expected JSON output.


def test_invalid_output_format():
    invalid_output = convert_yaml_or_json_to_format(
        sample_yaml_data, output_format='invalid_format')
    assert invalid_output is None


def test_invalid_data():
    invalid_data = "key1: value1, key2: value2"
    dot_output = convert_yaml_or_json_to_format(invalid_data,
                                                output_format='dot')
    json_output = convert_yaml_or_json_to_format(invalid_data,
                                                 output_format='json')
    assert dot_output is None
    assert json_output is None
