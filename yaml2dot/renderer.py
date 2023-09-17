import pydot
from typing import List, Dict, Any

# Create a global cache set to store generated data keys
CACHE = set()


def render(yaml_data: List[Dict[str, Any]], node_attrs=None) -> pydot.Dot:
    # Check if the input data is already in the cache
    data_key = str(yaml_data)  # Convert the list of dictionaries to a hashable key
    if data_key in CACHE:
        return None  # Return None to indicate that the result is cached

    if node_attrs is None:
        node_attrs = {
            "fontname": "Fira Mono",
            "fontsize": "10",
            "margin": "0.3,0.1",
            "fillcolor": "#fafafa",
            "shape": "box",
            "penwidth": "2.0",
            "style": "rounded,filled",
        }

    # Create an empty PyDot graph
    result = pydot.Dot(graph_type='digraph')

    for item in yaml_data:
        key = str(item["Key"])
        add_node(result, key, label=key, **node_attrs)
        if isinstance(item["Value"], (dict, list)):
            render_recursive(item["Value"], key, result, node_attrs)
        else:
            value = str(item["Value"])
            add_node(result, value, label=value)
            add_edge(result, key, value, arrowhead="none", penwidth="2.0")

    # Store the generated data key in the cache
    CACHE.add(data_key)

    return result

def add_node(graph, node_name, **kwargs):
    node = pydot.Node(node_name, **kwargs)
    graph.add_node(node)

def add_edge(graph, source, target, **kwargs):
    edge = pydot.Edge(source, target, **kwargs)
    graph.add_edge(edge)

def render_recursive(data, parent, graph, node_attrs):
    if isinstance(data, dict):
        for key, value in data.items():
            add_node(graph, key, label=key, **node_attrs)
            add_edge(graph, parent, key, arrowhead="none", penwidth="2.0")
            if isinstance(value, (dict, list)):
                render_recursive(value, key, graph, node_attrs)
            else:
                value_str = str(value)
                add_node(graph, value_str, label=value_str)
                add_edge(graph, key, value_str, arrowhead="none", penwidth="2.0")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                render_recursive(item, parent, graph, node_attrs)
            else:
                value_str = str(item)
                add_node(graph, value_str, label=value_str)
                add_edge(graph, parent, value_str, arrowhead="none", penwidth="2.0")
