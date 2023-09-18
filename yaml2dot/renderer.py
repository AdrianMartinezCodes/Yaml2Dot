import networkx as nx
from typing import Any

def render_yaml_structure(data: Any, graph: nx.MultiDiGraph, node_attrs, parent_node=None, rankdir="LR"):
    graph.graph['graph'] = {'rankdir': rankdir}  # Set the rankdir attribute for the graph

    def add_node_and_edge(node_name, parent):
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
                render_yaml_structure(value, graph, node_attrs, parent_node=child_node_name, rankdir=rankdir)
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
                        render_yaml_structure(value, graph, node_attrs, parent_node=child_node_name, rankdir=rankdir)
            else:
                child_node_name = str(item)
                add_node_and_edge(child_node_name, parent_node)

def render(yaml_data: Any, node_attrs=None, rankdir="LR") -> nx.MultiDiGraph:
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
