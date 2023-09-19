import filecmp
from pathlib import Path
import networkx as nx
import pytest
import yaml
import json

from yaml2dot.renderer import render

# Define a fixture to load example YAML or JSON files
@pytest.fixture(params=[
    "complex.yaml", "list.yaml", "mixed.yaml", "nested.yaml", "simple.yaml",
    "small_graph.yaml", "large_graph.yaml", "complex.yaml", "list.yaml",
])
def sample_data_file(request):
    # Construct the full path to the example data file (YAML or JSON)
    examples_dir = Path(__file__).resolve().parent.parent / "examples"
    data_file_path = examples_dir / request.param
    return str(data_file_path)

# Define a fixture to get the corresponding expected DOT file
@pytest.fixture
def expected_dot_file(sample_data_file):
    # Construct the full path to the expected DOT file in the tests directory
    tests_dir = Path(__file__).resolve().parent
    expected_dot_path = tests_dir / "expected-dot-files" / f"{Path(sample_data_file).stem}.dot"
    return str(expected_dot_path)

def test_render_with_example_files(sample_data_file, expected_dot_file):
    # Determine whether the file is in YAML or JSON format based on its extension
    file_extension = Path(sample_data_file).suffix.lower()
    
    if file_extension == '.yaml':
        with open(sample_data_file, "r") as data_file:
            data = yaml.safe_load(data_file)
    elif file_extension == '.json':
        with open(sample_data_file, "r") as data_file:
            data = json.load(data_file)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

    result = render(data)

    # Generate a DOT file from the result
    output_dot_file = "/tmp/output.dot"  # Use a temporary file for the generated DOT
    pydot_graph = nx.drawing.nx_pydot.to_pydot(result)
    pydot_graph.write_raw(output_dot_file)

    # Compare the generated DOT file with the expected DOT file
    assert filecmp.cmp(output_dot_file, expected_dot_file, shallow=False)
