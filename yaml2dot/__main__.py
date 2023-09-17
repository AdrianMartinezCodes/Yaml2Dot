import yaml
import click
from yaml2dot.renderer import render

@click.command()
@click.option("--input-file", type=click.File("r"), metavar="INPUT_FILE", required=True, help="Path to the input YAML file.")
@click.option("--output-file", type=click.File("w"), metavar="OUTPUT_FILE", required=True, help="Path to the output DOT file.")
def render_yaml(input_file, output_file):
    """
    Render YAML data as a graph and save it as a DOT file.

    Args:
        INPUT_FILE (str): Path to the input YAML file.
        OUTPUT_FILE (str): Path to the output DOT file.
    """
    yaml_data = yaml.load(input_file, Loader=yaml.FullLoader)
    pydot_graph = render(yaml_data)
    output_file.write(pydot_graph.to_string())

if __name__ == "__main__":
    render_yaml()
