# LEGACY CODE NOTICE
# ==============================================================================
# This file, legacy_renderer.py, contains legacy code that is no longer
# officially supported. It is included for backward compatibility reasons.
# Users are encouraged to use the updated version of this library for
# access to new features and ongoing support.
# ==============================================================================

from typing import Any, Dict

import networkx as nx


def create_graph(rankdir: str = "LR") -> nx.MultiDiGraph:
    """
    Creates a new directed graph with specified layout direction.

    Parameters:
    - rankdir (str, optional): The direction of the graph layout. Defaults to "LR" (left to right).

    Returns:
    - nx.MultiDiGraph: A new directed graph.
    """
    graph = nx.MultiDiGraph()
    graph.graph['graph'] = {'rankdir': rankdir}
    return graph


def add_node(graph: nx.MultiDiGraph, node_name: str, parent: str,
             node_attrs: Dict[str, Any]) -> None:
    """
    Adds a node and an edge to the graph.
    """
    if ":" in node_name and not (node_name.startswith('"') and
                                 node_name.endswith('"')):
        print(f"Quoting node name: {node_name}")
        node_name = f'"{node_name}"'

    graph.add_node(node_name, label=node_name, **node_attrs)

    if parent is not None:
        graph.add_edge(parent, node_name, arrowhead="none", penwidth="2.0")


def process_data(data: Any, graph: nx.MultiDiGraph, parent_node: str,
                 node_attrs: Dict[str, Any]) -> None:
    """
    Processes the data and adds nodes and edges to the graph.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            child_node_name = str(key)
            add_node(graph, child_node_name, parent_node, node_attrs)
            if isinstance(value, (dict, list)):
                process_data(value, graph, child_node_name, node_attrs)
            else:
                value_str = str(value)  # Convert simple values to string
                add_node(graph, value_str, child_node_name, node_attrs)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                process_data(item, graph, parent_node, node_attrs)
            else:
                item_str = str(item)  # Convert simple items to string
                add_node(graph, item_str, parent_node, node_attrs)


def render(data: Dict[str, Any],
           node_attrs: Dict[str, Any] = None,
           rankdir: str = "LR") -> nx.MultiDiGraph:
    """
    Renders a Python dictionary structure into a directed graph using NetworkX.

    Parameters:
    - data (Dict[str, Any]): The Python dictionary to render.
    - node_attrs (Dict[str, Any], optional): Attributes for each node. Defaults to predefined attributes.
    - rankdir (str, optional): The direction of the graph layout. Defaults to "LR" (left to right).

    Returns:
    - nx.MultiDiGraph: The resulting directed graph.
    """
    default_node_attrs = {
        "fontname": "Fira Mono",
        "fontsize": "10",
        "margin": "0.3,0.1",
        "fillcolor": "#fafafa",
        "shape": "box",
        "penwidth": 2.0,
        "style": "rounded",
    }
    final_node_attrs = node_attrs or default_node_attrs

    graph = create_graph(rankdir)
    process_data(data, graph, None, final_node_attrs)
    return graph
