import click
import json
import networkx as nx
from pathlib import Path
from yaml2dot.renderer import render
from yaml2dot.yaml_loader import parse_yaml
from networkx.readwrite import json_graph  # Import for JSON export

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
              help="Path to the output file (DOT or JSON).")
@click.option(
    "--rankdir",
    type=click.Choice(['LR', 'TB']),
    default='LR',
    help="Rank direction (LR for left to right, TB for top to bottom).")
@click.option(
    "--output-format",
    type=click.Choice(['dot', 'json']),
    default='dot',
    help="Output format (DOT or JSON).")
def render_yaml(input_file, output_file, rankdir, output_format):
    """
    Render YAML or JSON data as a graph and save it as a DOT or JSON file.

    Parameters:
    - input_file (click.Path): The input file (YAML or JSON) to be processed.
    - output_file (click.Path): The output file where the graph will be saved.
    - rankdir (str): Rank direction for the layout (LR for left to right, TB for top to bottom).
    - output_format (str): Output format (DOT or JSON).

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
            if isinstance(data, tuple) and data[1] is not None:
                click.echo(f"Error: {data[1]}", err=True)
                return
            if isinstance(data, tuple):
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

    if output_format == 'dot':
        # Save the graph as a DOT file
        pydot_graph = nx.drawing.nx_pydot.to_pydot(nx_graph)
        pydot_graph.write_raw(output_path)
    elif output_format == 'json':
        # Convert the graph to a JSON format
        json_data = json_graph.node_link_data(nx_graph)
        with open(output_path, 'w') as json_file:
            json.dump(json_data, json_file)

if __name__ == "__main__":
    render_yaml()
