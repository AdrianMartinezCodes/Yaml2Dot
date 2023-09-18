from typing import Any, Dict, List
import networkx as nx

def render_yaml_structure(data: Dict[str, Any],
                          graph: nx.MultiDiGraph,
                          node_attrs: Dict[str, Any],
                          parent_node: str = None,
                          rankdir: str = "LR") -> None:
    """
    Renders a Python dictionary structure into a directed graph using NetworkX.

    Parameters:
    - data (Dict[str, Any]): The Python dictionary to render.
    - graph (nx.MultiDiGraph): The NetworkX MultiDiGraph to render the data into.
    - node_attrs (Dict[str, Any]): A dictionary of attributes to apply to each node in the graph.
    - parent_node (str, optional): The parent node's name. Defaults to None.
    - rankdir (str, optional): The direction of the graph layout. Defaults to "LR" (left to right).

    Returns:
    - None
    """
    graph.graph['graph'] = {
        'rankdir': rankdir
    }

    def add_node_and_edge(node_name: str, parent: str) -> None:
        """
        Adds a node and an edge to the graph.

        Parameters:
        - node_name (str): The name of the node to add.
        - parent (str): The name of the parent node.

        Returns:
        - None
        """
        if ":" in node_name:
            node_name = f'"{node_name}"'
        graph.add_node(node_name, label=node_name, **node_attrs)
        if parent is not None:
            graph.add_edge(parent, node_name, arrowhead="none", penwidth="2.0")

    if isinstance(data, dict):
        for key, value in data.items():
            child_node_name = str(key)
            add_node_and_edge(child_node_name, parent_node)
            if not isinstance(value, (dict, list)):
                value_str = str(value)
                add_node_and_edge(value_str, child_node_name)
            else:
                render_yaml_structure(value,
                                      graph,
                                      node_attrs,
                                      parent_node=child_node_name,
                                      rankdir=rankdir)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                for key, value in item.items():
                    child_node_name = str(key)
                    add_node_and_edge(child_node_name, parent_node)
                    if not isinstance(value, (dict, list)):
                        value_str = str(value)
                        add_node_and_edge(value_str, child_node_name)
                    else:
                        render_yaml_structure(value,
                                              graph,
                                              node_attrs,
                                              parent_node=child_node_name,
                                              rankdir=rankdir)
            else:
                child_node_name = str(item)
                add_node_and_edge(child_node_name, parent_node)

def render(yaml_data: Dict[str, Any], node_attrs: Dict[str, Any] = None, rankdir: str = "LR") -> nx.MultiDiGraph:
    """
    Renders a Python dictionary structure into a directed graph using NetworkX.

    Parameters:
    - yaml_data (Dict[str, Any]): The Python dictionary to render.
    - node_attrs (Dict[str, Any], optional): A dictionary of attributes to apply to each node in the graph.
      Defaults to a predefined set of node attributes.
    - rankdir (str, optional): The direction of the graph layout. Defaults to "LR" (left to right).

    Returns:
    - nx.MultiDiGraph: The resulting directed graph.
    """
    if node_attrs is None:
        node_attrs = {
            "fontname": "Fira Mono",
            "fontsize": "10",
            "margin": "0.3,0.1",
            "fillcolor": "#fafafa",
            "shape": "box",
            "penwidth": 2.0,
            "style": "rounded",
        }

    result = nx.MultiDiGraph()
    render_yaml_structure(yaml_data, result, node_attrs, rankdir=rankdir)
    return result
