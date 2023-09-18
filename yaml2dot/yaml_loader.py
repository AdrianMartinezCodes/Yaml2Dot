import yaml
from typing import Any, Optional, Tuple, IO

def parse_yaml(reader: IO[str]) -> Tuple[Optional[dict], Optional[yaml.YAMLError]]:
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
