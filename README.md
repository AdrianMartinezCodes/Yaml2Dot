# pythonYaml2Dot
Python implementation of a yaml2dot converter.

Inspried by the original [yml2dot](https://github.com/lucasepe/yml2dot).

The **YAML to DOT Converter** is a Python tool that allows you to convert YAML data into a graph visualization represented in the DOT (Graph Description Language) format. It utilizes NetworkX for creating the graph structure and PyDot for generating DOT files.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
  - [Sample YAML Files](#sample-yaml-files)
  - [Rendering Example](#rendering-example)
- [Development](#development)
    - [Contributing](#contributing)
    - [Install](#dev-install)
    - [Testing](#testing)
- [License](#license)

## Getting Started

### Prerequisites

Before using the YAML to DOT Converter, ensure you have the following dependencies installed:

- Python 3.10(officially tested, unsure about older versions)
- [NetworkX](https://networkx.github.io/)
- [PyDot](https://pypi.org/project/pydot/)
- [Click](https://click.palletsprojects.com/en/8.0.x/)
### Installation
You can install NetworkX, PyDot, and Click using pip:

```bash
$pip install networkx pydot click
```

or you can simply clone the repository and navigate to the project directory:

```bash
$pip install .
```

## Usage

To convert a YAML file to a DOT file, use the following command:

```bash
python __main__.py --input-file INPUT_FILE --output-file OUTPUT_FILE [--rankdir RANKDIR]
```

* INPUT_FILE: Path to the input YAML file.
* OUTPUT_FILE: Path to the output DOT file.
* RANKDIR (optional): Rank direction (LR for left to right, TB for top to bottom). Default is LR.

Example usage:

```bash
python __main__.py --input-file input.yaml --output-file output.dot --rankdir LR
```
## Examples
### Sample YAML Files

The `examples` directory contains several sample YAML files that you can use for testing and experimentation. These files cover various YAML structures and complexities.

* complex.yaml: Complex YAML structure with nested dictionaries and lists.
* list.yaml: YAML data with a list of items.
* mixed.yaml: YAML data with a mix of dictionaries, lists, and values.
* nested.yaml: YAML data with nested dictionaries.
* simple.yaml: Simple YAML data with key-value pairs.
* small_graph.yaml: A small example YAML data.
* large_graph.yaml: A larger example YAML data.

### Rendering Example

To render a sample YAML file, use the following command:

```bash
python __main__.py --input-file examples/small_graph.yaml --output-file small_graph.dot --rankdir LR
```
This will generate a DOT file that can be visualized using Graphviz or other compatible tools.

## Development

### Contributing
Contributions are welcome! I don't have any formal contributing guidelines but since this is a fairly small project, feel free to send an informal message.


### Dev Install
The fastest way to start developing is to clone the repository and run the following command:
```bash
#pip install '.[all]'
```
### Testing

Simply run:
```bash
pytest
```


## License

This project is licensed under the MIT License. See the LICENSE file for details.
