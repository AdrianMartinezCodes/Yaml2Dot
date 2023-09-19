import click
import json
import networkx as nx
from pathlib import Path
from yaml2dot.renderer import render
from yaml2dot.yaml_loader import parse_yaml

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
              help="Path to the output DOT file.")
@click.option(
    "--rankdir",
    type=click.Choice(['LR', 'TB']),
    default='LR',
    help="Rank direction (LR for left to right, TB for top to bottom).")
def render_yaml(input_file, output_file, rankdir):
    """
    Render YAML or JSON data as a graph and save it as a DOT file.

    Parameters:
    - input_file (click.Path): The input file (YAML or JSON) to be processed.
    - output_file (click.Path): The output DOT file where the graph will be saved.
    - rankdir (str): Rank direction for the layout (LR for left to right, TB for top to bottom).
    
    Returns:
    - None
    """
    # Determine the file type based on the file extension
    file_extension = Path(input_file).suffix.lower()
    
    if file_extension == ".yaml" or file_extension == ".yml":
        load_function = parse_yaml
    elif file_extension == ".json":
        load_function = json.load  # Use json.load for JSON files
    else:
        raise click.BadParameter("Invalid input file format. Supported formats: YAML (.yaml, .yml) and JSON (.json)")

    # Load the data from the input file
    try:
        with open(input_file, "r") as file:
            data = load_function(file)
            if isinstance(data,tuple) and data[1] is not None:
                click.echo(f"Error: {data[1]}", err=True)
                return
            if isinstance(data,tuple):
                data = data[0]
    except json.JSONDecodeError as e:
        click.echo(f"Error parsing JSON: {e}", err=True)
        return
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        return
    nx_graph = render(data, rankdir=rankdir)

    # Create the directory for the output file if it doesn't exist
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pydot_graph = nx.drawing.nx_pydot.to_pydot(nx_graph)
    pydot_graph.write_raw(output_path)

if __name__ == "__main__":
    render_yaml()
