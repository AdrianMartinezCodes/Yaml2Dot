from pathlib import Path

import click
import networkx as nx

from yaml2dot.renderer import render
from yaml2dot.yaml_loader import parse_yaml 

@click.command()
@click.option("--input-file",
              type=click.File("r"),
              metavar="INPUT_FILE",
              required=True,
              help="Path to the input YAML file.")
@click.option("--output-file",
              type=click.Path(),
              metavar="OUTPUT_FILE",
              required=True,
              help="Path to the output DOT file.")
@click.option(
    "--rankdir",
    type=click.Choice(['LR', 'TB']),
    default='LR',
    help="Rank direction (LR for left to right, TB for top to bottom).")
def render_yaml(input_file, output_file, rankdir):
    """
    Render YAML data as a graph and save it as a DOT file.

    Parameters:
    - input_file (click.File): The input YAML file to be processed.
    - output_file (click.Path): The output DOT file where the graph will be saved.
    - rankdir (str): Rank direction for the layout (LR for left to right, TB for top to bottom).
    
    Returns:
    - None
    """
    yaml_data, yaml_error = parse_yaml(input_file)
    if yaml_error:
        click.echo(f"Error parsing YAML: {yaml_error}", err=True)
        return 1

    nx_graph = render(yaml_data, rankdir=rankdir)

    # Create the directory for the output file if it doesn't exist
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pydot_graph = nx.drawing.nx_pydot.to_pydot(nx_graph)
    pydot_graph.write_raw(output_path)

if __name__ == "__main__":
    render_yaml()
