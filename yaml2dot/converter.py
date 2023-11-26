import json
from typing import Optional, Union

import networkx as nx
from networkx.readwrite import json_graph

from yaml2dot.renderer import render


def convert_yaml_or_json_to_format(data: Union[dict, None],
                                   output_format: str = 'dot',
                                   rankdir: str = 'LR') -> Optional[str]:
    """
    Convert YAML or JSON data to DOT or JSON format.

    Parameters:
    - data (Union[dict, None]): The input YAML or JSON data as a dictionary or None if there was an error.
    - output_format (str): Output format ('dot' or 'json'). Default is 'dot'.
    - rankdir (str): Rank direction for the layout (LR for left to right, TB for top to bottom). Default is 'LR'.

    Returns:
    - Optional[str]: The converted data in DOT or JSON format as a string or None if there was an error.
    """
    if data is None:
        return None

    if not isinstance(data, dict):
        return None
    # We can probably include more data validations

    nx_graph = render(data, rankdir=rankdir)

    if output_format == 'dot':
        # Convert the graph to DOT format
        pydot_graph = nx.drawing.nx_pydot.to_pydot(nx_graph)
        return pydot_graph.to_string()
    elif output_format == 'json':
        # Convert the graph to JSON format
        json_data = json_graph.node_link_data(nx_graph)
        return json.dumps(json_data, indent=2)

    return None
