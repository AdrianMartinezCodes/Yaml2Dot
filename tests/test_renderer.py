import networkx as nx
import pytest
import yaml
from yaml2dot.renderer import render
from pathlib import Path
import filecmp

# Define a fixture to load example YAML files
@pytest.fixture(params=["complex.yaml", "list.yaml", "mixed.yaml", "nested.yaml", "simple.yaml", "small_graph.yaml", "large_graph.yaml"])
def sample_yaml_file(request):
    # Construct the full path to the example YAML file
    examples_dir = Path(__file__).resolve().parent.parent / "examples"
    yaml_file_path = examples_dir / request.param
    return str(yaml_file_path)

# Define a fixture to get the corresponding expected DOT file
@pytest.fixture
def expected_dot_file(sample_yaml_file):
    # Construct the full path to the expected DOT file in the tests directory
    tests_dir = Path(__file__).resolve().parent
    expected_dot_path = tests_dir / "expected_dot_files" / f"{Path(sample_yaml_file).stem}.dot"
    return str(expected_dot_path)

def test_render_with_example_files(sample_yaml_file, expected_dot_file):
    with open(sample_yaml_file, "r") as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    result = render(yaml_data)

    # Generate a DOT file from the result
    output_dot_file = "/tmp/output.dot"  # Use a temporary file for the generated DOT
    pydot_graph = nx.drawing.nx_pydot.to_pydot(result)
    pydot_graph.write_raw(output_dot_file)

    # Compare the generated DOT file with the expected DOT file
    assert filecmp.cmp(output_dot_file, expected_dot_file, shallow=False)
