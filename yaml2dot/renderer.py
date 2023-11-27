from collections import deque
from typing import Any, Dict, Final, List, Union

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
    # Handle empty node names or other specific conditions
    if not node_name.strip():
        # Skip adding the node, or handle it differently based on your requirements
        return
    # Existing code to handle colons in node names
    if ":" in node_name and not (node_name.startswith('"') and
                                 node_name.endswith('"')):
        node_name = node_name.replace(":", HANDLE_COLON)

    graph.add_node(node_name, label=node_name, **node_attrs)

    if parent is not None:
        if ":" in parent and not (parent.startswith('"') and
                                  parent.endswith('"')):
            parent = f'"{parent}"'
        graph.add_edge(parent, node_name, arrowhead="none", penwidth="2.0")


def process_data_bfs(data: Any,
                     graph: nx.MultiDiGraph,
                     node_attrs: Dict[str, Any],
                     file_num=0,
                     multi_view=False,
                     first_level=False) -> None:
    if multi_view:
        node = [(data, "", None)]
    else:
        node = [(data, str(file_num), None)]
    queue = deque(node)  # Initialize with the root data

    while queue:
        current_data, parent_path, parent_node = queue.popleft()

        if isinstance(current_data, dict):
            if first_level:
                first_level = False
                items = reversed(current_data.items())
            else:
                items = current_data.items()
            for key, value in items:
                child_path = f"{parent_path}{SEPARATOR}{key}" if parent_path else key
                if not graph.has_node(child_path):
                    add_node(graph, child_path, parent_node, node_attrs)

                # Process the value
                if isinstance(value, (dict, list)):
                    queue.append((value, child_path, child_path))
                else:
                    value_path = f"{child_path}{SEPARATOR}{value}"
                    if not graph.has_node(value_path):
                        add_node(graph, value_path, child_path, node_attrs)

        elif isinstance(current_data, list):
            for item in current_data[::-1]:
                if isinstance(item, (dict, list)):
                    # Enqueue the item for processing without creating a separate node for the index
                    item_path = f"{parent_path}{SEPARATOR}{item}"  # Unique path for each item
                    if not graph.has_node(item_path):
                        queue.append((item, parent_path, parent_path))
                else:
                    # Process simple list items as values directly under the parent
                    value_path = f"{parent_path}{SEPARATOR}{item}"
                    if not graph.has_node(value_path):
                        add_node(graph, value_path, parent_path, node_attrs)


def rename_nodes_for_rendering(graph: nx.MultiDiGraph) -> None:
    """
    Renames nodes for rendering by using only the last part of the path as the label.
    """
    for node in graph.nodes:
        # Use only the last part of the path as the label
        new_label = node.split(SEPARATOR)[-1]
        if "---" in new_label:
            new_label = new_label.replace(HANDLE_COLON, ":")
            new_label = f'"{new_label}"'
        graph.nodes[node]['label'] = new_label


def render(data: List[Dict[str, Any]],
           user_node_attrs: Dict[str, Any] = None,
           rankdir: str = "LR",
           multi_view=False,
           round_robin=False,
           shape="rounded") -> nx.MultiDiGraph:
    """
    Renders a list of Python dictionaries (from YAML documents) into a directed graph using NetworkX.

    Parameters:
    - data (List[Dict[str, Any]]): The list of Python dictionaries to render, each representing a YAML document.
    - user_node_attrs (Dict[str, Any], optional): User-defined attributes for each node.
    - rankdir (str, optional): The direction of the graph layout. Defaults to "LR" (left to right).
    - multi_view (bool, optional): Flag to indicate multiple YAML document rendering. Disables round robin style.
    - round_robin (bool,optional): Flag to indicate if the library will assign node shapes automatically
    - shape (str,optional): User specified custom shape for nodes. This option is ignored if round_robin is True.

    Returns:
    - nx.MultiDiGraph: The resulting directed graph.
    """
    graph = create_graph(rankdir)

    # Define default node attributes if not provided by the user
    default_node_attrs = {
        "fontname": "Fira Mono",
        "fontsize": "10",
        "margin": "0.3,0.1",
        "fillcolor": "#fafafa",
        "penwidth": 2.0,
        "style": "rounded",
        "shape": shape
    }
    data = [data] if not isinstance(data, list) else data
    node_attrs = {**default_node_attrs, **(user_node_attrs or {})}
    if multi_view:
        round_robin = False

    shapes = ["rounded", "ellipse"]
    for index, document in enumerate(reversed(data)):
        # Select shape in a round-robin fashion from the shapes list
        if round_robin:
            shape = shapes[index % len(shapes)]
            # Update node attributes with the selected shape for this document
            document_node_attrs = {**node_attrs, "shape": shape}
        else:
            document_node_attrs = node_attrs
        process_data_bfs(document,
                         graph,
                         document_node_attrs,
                         file_num=index,
                         multi_view=multi_view,
                         first_level=True)

    rename_nodes_for_rendering(graph)
    return graph
