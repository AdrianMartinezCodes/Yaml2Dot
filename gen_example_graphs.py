import os
import networkx as nx
from yaml2dot.renderer import render
import yaml
from pathlib import Path

# Define the directory containing the sample YAML files
yaml_dir = Path("examples")

# Define the directory to store the generated DOT files
dot_dir = Path("tests/expected_dot_files")

# Ensure the output directory exists
dot_dir.mkdir(parents=True, exist_ok=True)

# List of sample YAML files
yaml_files = [
    "complex.yaml",
    "list.yaml",
    "mixed.yaml",
    "nested.yaml",
    "simple.yaml",
    "small_graph.yaml",
    "large_graph.yaml",
]

# Loop through the YAML files and generate DOT files
for yaml_file in yaml_files:
    # Load the YAML data
    with open(yaml_dir / yaml_file, "r") as file:
        yaml_data = yaml.safe_load(file)

    # Render YAML data as a graph
    nx_graph = render(yaml_data)

    # Generate a DOT file from the graph
    dot_filename = Path(os.path.splitext(yaml_file)[0] + ".dot")
    dot_filepath = dot_dir / dot_filename

    pydot_graph = nx.drawing.nx_pydot.to_pydot(nx_graph)
    pydot_graph.write_raw(dot_filepath)

    print(f"Generated DOT file: {dot_filepath}")

print("DOT file generation complete.")
