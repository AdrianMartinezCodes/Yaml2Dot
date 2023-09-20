import json
from typing import IO, Any, Optional, Tuple

import yaml


def parse_yaml(
        reader: IO[str]) -> Tuple[Optional[dict], Optional[yaml.YAMLError]]:
    """
    Parse YAML data from a file-like object and return the parsed dictionary and any parsing error.

    Parameters:
    - reader (IO[str]): A file-like object containing YAML data.

    Returns:
    - Tuple[Optional[dict], Optional[yaml.YAMLError]]: A tuple containing the parsed dictionary
      (or None if there was an error) and any parsing error (or None if parsing was successful).
    """
    try:
        parsed_yaml = yaml.safe_load(reader)
        return parsed_yaml, None
    except yaml.YAMLError as error:
        return None, error


def load_yaml_or_json(file_path: str) -> Optional[dict]:
    """
    Load YAML or JSON data from a file and return the parsed dictionary.

    Parameters:
    - file_path (str): The path to the input YAML or JSON file.

    Returns:
    - Optional[dict]: The parsed dictionary or None if there was an error.
    """
    file_extension = file_path.lower().split('.')[-1]

    if file_extension in ('yaml', 'yml'):
        with open(file_path, 'r') as file:
            parsed_data, error = parse_yaml(file)
            if error:
                print(f"Error parsing YAML: {error}")
            return parsed_data
    elif file_extension == 'json':
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as error:
            print(f"Error parsing JSON: {error}")
    else:
        print(
            "Invalid file format. Supported formats: YAML (.yaml, .yml) and JSON (.json)"
        )
        return None
