import json
from pathlib import Path

import click
import networkx as nx
from networkx.readwrite import json_graph

from yaml2dot.data_loader import load_yaml_or_json
from yaml2dot.renderer import render


@click.command()
@click.option("--input-file",
              type=click.Path(exists=True),
              metavar="INPUT_FILE",
              required=True,
              help="Path to the input YAML or JSON file.")
@click.option("--output-file",
              type=click.Path(),
              metavar="OUTPUT_FILE",
              required=True,
              help="Path to the output file. Use '-' for stdout JSON format.")
@click.option(
    "--rankdir",
    type=click.Choice(['LR', 'TB']),
    default='LR',
    help="Rank direction (LR for left to right, TB for top to bottom).")
@click.option("--output-format",
              type=click.Choice(['dot', 'json', '']),
              default='dot',
              help="Output format (DOT or JSON).")
@click.option(
    "--multi-view",
    is_flag=True,
    help=
    "Enable alternative graph view for multiple YAML documents. Disables round robin."
)
@click.option(
    "--round-robin",
    is_flag=True,
    help="Enable Round Robin Node Style. If not, defaults to 'rounded' shape.")
@click.option(
    "--shape",
    type=click.STRING,
    default="rounded",
    help=
    "User defined node shape. Default='rounded'. See graphviz page: https://graphviz.org/doc/info/shapes.html for support shapes."
)
def render_yaml(input_file, output_file, rankdir, output_format, multi_view,
                round_robin, shape):
    """
    Render YAML or JSON data as a graph and save it as a DOT or JSON file.

    Parameters:
    - input_file (click.Path): The input file (YAML or JSON) to be processed.
    - output_file (click.Path): The output file where the graph will be saved.
    - rankdir (str): Rank direction for the layout (LR for left to right, TB for top to bottom).
    - output_format (str): Output format (DOT or JSON).
    - multi_view (bool): Flag to enable alternative graph view for multiple YAML documents.
    - round_robin (bool): Flag to enable Round Robin Node Style.
    - shape (str): User defined node shape.

    Returns:
    - None
    """
    data = load_yaml_or_json(input_file)

    if data is None:
        return

    nx_graph = render(data,
                      rankdir=rankdir,
                      multi_view=multi_view,
                      round_robin=round_robin,
                      shape=str(shape))

    if output_file != "-":
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_format == 'dot':
        pydot_graph = nx.drawing.nx_pydot.to_pydot(nx_graph)
        pydot_graph.write_raw(output_path)
    elif output_format == 'json':
        if output_file == "-":
            json_data = json_graph.node_link_data(nx_graph)
            click.echo(json.dumps(json_data, indent=2))
        else:
            with open(output_path, 'w') as json_file:
                json_data = json_graph.node_link_data(nx_graph)
                json.dump(json_data, json_file, indent=2)


if __name__ == "__main__":
    render_yaml()
