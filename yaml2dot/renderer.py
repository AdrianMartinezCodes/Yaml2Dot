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
    if ":" in node_name and not (node_name.startswith('"') and
                                 node_name.endswith('"')):
        node_name = node_name.replace(":", "-")
    graph.add_node(node_name, label=node_name, **node_attrs)
    if parent is not None:
        # Ensure parent name is correctly formatted
        if ":" in parent and not (parent.startswith('"') and
                                  parent.endswith('"')):
            parent = f'"{parent}"'
        graph.add_edge(parent, node_name, arrowhead="none", penwidth="2.0")


def process_data(data: Any, graph: nx.MultiDiGraph, parent_path: str | None,
                 node_attrs: Dict[str, Any]) -> None:
    """
    Processes the data and adds nodes and edges to the graph.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            child_path = f"{parent_path}/{key}" if parent_path else key
            add_node(graph, child_path, parent_path, node_attrs)
            if isinstance(value, (dict, list)):
                process_data(value, graph, child_path, node_attrs)
            else:
                value_str = str(value)
                value_path = f"{child_path}/{value_str}"
                add_node(graph, value_path, child_path, node_attrs)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            item_path = f"{parent_path}/{str(index)}/{parent_path}"
            if isinstance(item, (dict, list)):
                process_data(item, graph, item_path, node_attrs)
            else:
                item_str = str(item)
                add_node(graph, item_str, item_path, node_attrs)


def rename_nodes_for_rendering(graph: nx.MultiDiGraph) -> None:
    """
    Renames nodes for rendering by using only the last part of the path as the label.
    """
    for node in graph.nodes:
        # Use only the last part of the path as the label
        new_label = node.split('/')[-1]
        graph.nodes[node]['label'] = new_label


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
    rename_nodes_for_rendering(graph)
    return graph
