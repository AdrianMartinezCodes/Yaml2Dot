import json
from typing import Optional, Union

import networkx as nx
from networkx.readwrite import json_graph

from yaml2dot.renderer import render


def convert_yaml_or_json_to_format(data: Union[dict, None],
                                   user_node_attrs: dict = None,
                                   output_format: str = 'dot',
                                   rankdir: str = 'LR',
                                   multi_view: bool = False,
                                   round_robin: bool = False,
                                   shape: str = 'rounded') -> Optional[str]:
    """
    Convert YAML or JSON data to DOT or JSON format.

    Parameters:
    - data (Union[dict, None]): The input YAML or JSON data as a dictionary or None if there was an error.
    - user_node_attrs (Dict[str, Any], optional): User-defined attributes for each node.
    - output_format (str): Output format ('dot' or 'json'). Default is 'dot'.
    - rankdir (str): Rank direction for the layout (LR for left to right, TB for top to bottom). Default is 'LR'.
    - multi_view (bool): Enable alternative graph view for multiple YAML documents. Default is False.
    - round_robin (bool): Enable Round Robin Node Style. If not, defaults to user-defined shapes. Default is False.
    - shape (str): User-defined node shape. Default is 'rounded'.

    Returns:
    - Optional[str]: The converted data in DOT or JSON format as a string or None if there was an error.
    """
    if data is None or (not isinstance(data, dict) and not isinstance(data,list)):
        return None
    nx_graph = render(data,
                      user_node_attrs=user_node_attrs,
                      rankdir=rankdir,
                      multi_view=multi_view,
                      round_robin=round_robin,
                      shape=shape)

    if output_format == 'dot':
        # Convert the graph to DOT format
        pydot_graph = nx.drawing.nx_pydot.to_pydot(nx_graph)
        return pydot_graph.to_string()
    elif output_format == 'json':
        # Convert the graph to JSON format
        json_data = json_graph.node_link_data(nx_graph)
        return json.dumps(json_data, indent=2)

    return None
