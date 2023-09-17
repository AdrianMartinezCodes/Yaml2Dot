import networkx as nx
import pydot
import pytest
from yaml2dot.renderer import render
from tests.generate_large_graph import generate_large_graph

@pytest.fixture
def sample_yaml_data():
    return [
        {'Key': 'key1', 'Value': 'value1'},
        {'Key': 'key2', 'Value': {'nested_key': 'nested_value'}},
        {'Key': 'key3', 'Value': [1, 2, 3]},
    ]

def test_render_basic(sample_yaml_data):
    result = render(sample_yaml_data)
    assert isinstance(result, pydot.Dot)
    assert len(result.get_nodes()) == 9  
    assert len(result.get_edges()) == 6   

def test_render_with_cache(sample_yaml_data):
    result1 = render(sample_yaml_data)
    result2 = render(sample_yaml_data)  # Rendering the same data again

    assert result1 is result2  # The result should be cached and the same object

def test_render_empty_data():
    empty_data = []
    result = render(empty_data)
    
    assert isinstance(result, pydot.Dot)  # Updated to check for PyDot graph
    assert len(result.get_nodes()) == 0   # Updated to check the number of nodes

def test_generate_large_graph():
    random_seed = 42  # Set your desired random seed
    num_nodes = 1000  # Set the number of nodes for the large graph
    large_graph = generate_large_graph(num_nodes, random_seed)

    assert isinstance(large_graph, nx.DiGraph)
    assert large_graph.number_of_nodes() == num_nodes