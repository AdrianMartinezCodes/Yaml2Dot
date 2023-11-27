import filecmp
import json
import tempfile
from pathlib import Path

import networkx as nx
import pytest
import yaml

from yaml2dot.renderer import render


@pytest.fixture(params=[
    "complex.yaml", "list.yaml", "mixed.yaml", "nested.yaml", "simple.yaml",
    "small_graph.yaml", "large_graph.yaml", "list.yaml", "k8-deployment.yaml"
])
def sample_data_file(request):
    examples_dir = Path(__file__).resolve().parent.parent / "examples"
    data_file_path = examples_dir / request.param
    return str(data_file_path)


@pytest.fixture
def expected_dot_file(sample_data_file):
    tests_dir = Path(__file__).resolve().parent
    expected_dot_path = tests_dir / "expected-dot-files" / f"{Path(sample_data_file).stem}.dot"
    return str(expected_dot_path)


def test_render_with_example_files(sample_data_file, expected_dot_file):
    file_extension = Path(sample_data_file).suffix.lower()

    if file_extension == '.yaml':
        with open(sample_data_file, "r") as data_file:
            data = list(yaml.safe_load_all(data_file))
    elif file_extension == '.json':
        with open(sample_data_file, "r") as data_file:
            data = json.load(data_file)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
    if Path(sample_data_file).stem == "k8-deployment":
        result = render(data, round_robin=True)
    else:
        result = render(data)

    # Create a temporary directory for the DOT output
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate a DOT file in the temporary directory
        output_dot_file = Path(temp_dir) / "output.dot"
        pydot_graph = nx.drawing.nx_pydot.to_pydot(result)
        pydot_graph.write_raw(str(output_dot_file))

        # Compare the generated DOT file with the expected DOT file
        assert filecmp.cmp(output_dot_file, expected_dot_file, shallow=False)
