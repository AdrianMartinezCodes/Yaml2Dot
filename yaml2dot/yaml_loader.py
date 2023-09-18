import yaml


def parse_yaml(reader):
    try:
        parsed_yaml = yaml.safe_load(reader)
        return parsed_yaml, None
    except yaml.YAMLError as error:
        return None, error
