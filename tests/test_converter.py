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
                                                output_format='dot',
                                                multi_view=False,
                                                round_robin=False,
                                                shape='rounded')
    assert dot_output is not None
    assert isinstance(dot_output, str)
    assert "shape=rounded" in dot_output


def test_convert_yaml_to_json():
    json_output = convert_yaml_or_json_to_format(sample_yaml_data,
                                                 output_format='json')
    assert json_output is not None
    assert isinstance(json_output, str)
    assert "nodes" in json_output


def test_convert_json_to_dot():
    dot_output = convert_yaml_or_json_to_format(sample_json_data,
                                                output_format='dot')
    assert dot_output is not None
    assert isinstance(dot_output, str)


def test_convert_json_to_json():
    json_output = convert_yaml_or_json_to_format(sample_json_data,
                                                 output_format='json')
    assert json_output is not None
    assert isinstance(json_output, str)
    assert "nodes" in json_output


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


def test_convert_with_custom_node_attrs():
    custom_attrs = {"color": "red", "style": "filled"}
    dot_output = convert_yaml_or_json_to_format(sample_yaml_data,
                                                output_format='dot',
                                                user_node_attrs=custom_attrs)
    assert dot_output is not None
    assert "color=red" in dot_output
    assert "style=filled" in dot_output


def test_convert_with_multi_view():
    dot_output = convert_yaml_or_json_to_format(sample_yaml_data,
                                                output_format='dot',
                                                multi_view=True)
    assert dot_output is not None


def test_convert_with_round_robin():
    dot_output = convert_yaml_or_json_to_format(sample_yaml_data,
                                                output_format='dot',
                                                round_robin=True)
    assert dot_output is not None


def test_convert_with_specific_shape():
    shape = "box"
    dot_output = convert_yaml_or_json_to_format(sample_yaml_data,
                                                output_format='dot',
                                                shape=shape)
    assert dot_output is not None
    assert "shape=box" in dot_output

def test_read_list_inputs():
    raw_list = [{'apiVersion': 'v1', 'kind': 'Namespace', 'metadata': {'name': 'example-namespace'}}, {'apiVersion': 'v1', 'kind': 'ConfigMap', 'metadata': {'name': 'example-config', 'namespace': 'example-namespace'}, 'data': {'application.properties': 'property1=value1\nproperty2=value2\n'}}, {'apiVersion': 'apps/v1', 'kind': 'Deployment', 'metadata': {'name': 'example-deployment', 'namespace': 'example-namespace'}, 'spec': {'replicas': 3, 'selector': {'matchLabels': {'app': 'example'}}, 'template': {'metadata': {'labels': {'app': 'example'}}, 'spec': {'containers': [{'name': 'example-container', 'image': 'example-image:latest', 'ports': [{'containerPort': 8080}], 'envFrom': [{'configMapRef': {'name': 'example-config'}}]}]}}}}, {'apiVersion': 'v1', 'kind': 'Service', 'metadata': {'name': 'example-service', 'namespace': 'example-namespace'}, 'spec': {'selector': {'app': 'example'}, 'ports': [{'protocol': 'TCP', 'port': 80, 'targetPort': 8080}], 'type': 'LoadBalancer'}}]
    assert convert_yaml_or_json_to_format(raw_list)