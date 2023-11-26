from typing import Any, Dict, Union , Final
from collections import deque
import networkx as nx

SEPARATOR: Final = "__"
HANDLE_COLON: Final = "---"

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
        node_name = node_name.replace(":", HANDLE_COLON)
    graph.add_node(node_name, label=node_name, **node_attrs)
    if parent is not None:
        # Ensure parent name is correctly formatted
        if ":" in parent and not (parent.startswith('"') and
                                  parent.endswith('"')):
            parent = f'"{parent}"'
        graph.add_edge(parent, node_name, arrowhead="none", penwidth="2.0")



def process_data_bfs(data: Any, graph: nx.MultiDiGraph, node_attrs: Dict[str, Any]) -> None:
    queue = deque([(data, "", None)])  # Initialize with the root data

    while queue:
        current_data, parent_path, parent_node = queue.popleft()

        if isinstance(current_data, dict):
            for key, value in current_data.items():
                child_path = f"{parent_path}{SEPARATOR}{key}" if parent_path else key
                add_node(graph, child_path, parent_node, node_attrs)
                
                # Process the value
                if isinstance(value, (dict, list)):
                    queue.append((value, child_path, child_path))
                else:
                    value_path = f"{child_path}{SEPARATOR}{value}"
                    add_node(graph, value_path, child_path, node_attrs)

        elif isinstance(current_data, list):
            for index, item in enumerate(current_data):
                item_path = f"{parent_path}{SEPARATOR}{index}"
                add_node(graph, item_path, parent_node, node_attrs)
                if isinstance(item, (dict, list)):
                    queue.append((item, item_path, item_path))
                else:
                    # Process simple list items as values
                    value_path = f"{item_path}{SEPARATOR}{item}"
                    add_node(graph, value_path, item_path, node_attrs)


def rename_nodes_for_rendering(graph: nx.MultiDiGraph) -> None:
    """
    Renames nodes for rendering by using only the last part of the path as the label.
    """
    for node in graph.nodes:
        # Use only the last part of the path as the label
        new_label = node.split(SEPARATOR)[-1]
        if "---" in new_label:
            new_label = new_label.replace(HANDLE_COLON,":")
            new_label = f'"{new_label}"'
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
    process_data_bfs(data, graph, final_node_attrs)
    rename_nodes_for_rendering(graph)
    return graph
