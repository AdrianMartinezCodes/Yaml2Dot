import os
from pathlib import Path
import json
import yaml
import networkx as nx
from yaml2dot.renderer import render

# Define the directory containing the sample YAML and JSON files
data_dir = Path("examples")

# Define the directory to store the generated DOT files
dot_dir = Path("tests/expected-dot-files")

# Ensure the output directory exists
dot_dir.mkdir(parents=True, exist_ok=True)

# List of sample files (both YAML and JSON)
file_extensions = [".yaml", ".json",".yml"]

# Loop through the files and generate DOT files
for file_extension in file_extensions:
    # Find all files with the specified extension
    data_files = [f for f in data_dir.glob(f"*{file_extension}")]

    for data_file in data_files:
        # Load the data (JSON or YAML)
        if file_extension == ".json":
            with open(data_file, "r") as file:
                data = json.load(file)
        elif file_extension in [".yaml",".yml"]:
            with open(data_file, "r") as file:
                data = list(yaml.safe_load_all(file))
        # Render data as a graph
        nx_graph = render(data)

        # Generate a DOT file from the graph
        dot_filename = data_file.stem + ".dot"
        dot_filepath = dot_dir / dot_filename

        pydot_graph = nx.drawing.nx_pydot.to_pydot(nx_graph)
        pydot_graph.write_raw(dot_filepath)

        print(f"Generated DOT file: {dot_filepath}")

print("DOT file generation complete.")
