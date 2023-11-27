# Yaml2Dot

Python implementation of a yaml2dot converter. Now with JSON Support and enhcanched node customization!

Check out a demo at my personal page [teamayejay.com/Adrian/Yaml2Dot](https://teamayejay.com/Adrian/Yaml2Dot).

Inspried by the original [yml2dot](https://github.com/lucasepe/yml2dot).

The YAML to DOT Converter is a Python utility designed to transform YAML or JSON data into a visual graph representation, available in either the DOT (Graph Description Language) or JSON format. This tool employs NetworkX to construct the graph structure and offers the flexibility to produce either DOT files or JSON output in the form of node-link data.

Transform this data:

```yaml
person:
  name: Alice
  age: 28
  address:
    street: 456 Elm St
    city: Another Town
    zip: '54321'
  hobbies:
    - reading
    - hiking
```
into this easy to read graph(after rendering using d3-graphviz):

![Nested Yaml](/examples/nested.svg)

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [CLI OPTIONS](#cli-options)
- [Examples](#examples)
  - [Sample YAML Files](#sample-yaml-files)
  - [Sample JSON File](#sample-json-file)
  - [Rendering Example](#rendering-example)
- [Development](#development)
  - [Contributing](#contributing)
  - [Install](#dev-install)
  - [Testing](#testing)
- [License](#license)


## Getting Started

### Prerequisites

Before using the YAML to DOT Converter, ensure you have the following dependencies installed:

- Python 3.10(officially tested)
- [NetworkX](https://networkx.github.io/)
- [PyDot](https://pypi.org/project/pydot/)
- [Click](https://click.palletsprojects.com/en/8.0.x/)

### Installation

The most straightforward way to install is to use pip:

```bash
pip install yaml2dot
```

For a manual install you can setup a virtual environment and do the following:

```bash
pip install networkx pydot click
```

or clone the repository and navigate to the project directory:

```bash
pip install .
```

## Usage

To convert a YAML/JSON file to a DOT file, use the following command:

```bash
yaml2dot --input-file INPUT_FILE --output-file OUTPUT_FILE [--rankdir RANKDIR] [--output-format OUTPUT_FORMAT] [--multi-view] [--round-robin] [--shape SHAPE]

```

- INPUT_FILE: Path to the input YAML/JSON file.
- OUTPUT_FILE: Path to the output DOT file.
- RANKDIR (optional): Rank direction (LR for left to right, TB for top to bottom). Default is LR.
- MULTI-VIEW (optional): Enable alternative graph view for multiple YAML documents.
- ROUND-ROBIN (optional): Enable round-robin node style selection. If not specified, defaults the rounded shape.
- SHAPE (optional): User-defined node shape, applicable when round-robin is not used. See [Graphviz Shapes](https://graphviz.org/doc/info/shapes.html) for supported shapes.

Example usage for conerting to DOT:

```bash
yaml2dot --input-file input.yaml --output-file output.dot --rankdir LR
```

Example usage for converting for node link data JSON:

```base
yaml2dot --input-file input.json --output-file output.json --output-format json
```

Here's an example of how to use the library's API to convert YAML or JSON data:

```python
from yaml2dot import data_loader,converter

# Load YAML or JSON data from a file
data = data_loader.load_yaml_or_json('input.yaml')
# or input a python dict directly
# data = {"example":"example"}

# Convert the data to DOT format (default)
dot_output = converter.convert_yaml_or_json_to_format(data)

# Convert the data to JSON format
json_output = converter.convert_yaml_or_json_to_format(data, output_format='json')

# Print or save the outputs as needed
print(dot_output)
print(json_output)
```


### CLI Options

The yaml2dot command offers various options to customize the graph rendering:

- `--round-robin`: Automatically assigns different node shapes in a round-robin fashion for each YAML document.
- `--shape`: Specify a custom shape for nodes. This option is ignored if --round-robin is used.
- `--multi-view`: Useful for rendering multiple YAML documents in a single file with distinct node styles. Disables round-robin.



## Examples

### Sample YAML/JSON Files

The `examples` directory contains several sample YAML files that you can use for testing and experimentation. These files cover various YAML structures and complexities. It also contain an example json file for testing and experimentation.
  

### Rendering Example

To render a sample YAML/JSON file, use the following command:

```bash
yaml2dot --input-file examples/small_graph.yaml --output-file small_graph.dot --rankdir LR --shape diamond
```

This will generate a DOT file that can be visualized using Graphviz or other compatible tools.

To render to JSON format:

```bash
yaml2dot --input-file examples/small_graph.yaml --output-file small_graph.json --rankdir LR --output-format json 
```

This will generate a node link data JSON file of the networkx graph that can be visualzied using [d3](https://d3js.org/).

For a round-robin node style in multi-document YAMLS:

```bash
yaml2dot --input-file examples/multi_document.yaml --output-file multi_document.dot --rankdir LR --multi-view --round-robin
```

## Development

### Contributing

Contributions are welcome! I don't have any formal contributing guidelines but since this is a fairly small project, feel free to send an informal message.

### Dev Install

The fastest way to start developing is to clone the repository and run the following command:

```bash
pip install '.[all]'
```

### Testing

Simply run:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
