import configparser
import json
import os
from enum import Enum
from typing import Dict, List, Optional, Union


# =========================================================================== #

class ConfigType(Enum):
    MAIN = 'config.ini'
    SECRETS = 'secrets.ini'


# =========================================================================== #

def get_config_val(
    section: str,
    key: str,
    config_type: Optional[ConfigType] = ConfigType.MAIN,
) -> Union[str, int, float]:
    """Retrieve and convert a value from .ini config file."""
    config_path = os.path.join('..', 'cfg', config_type.value)
    ConfigParser = configparser.ConfigParser()
    ConfigParser.read(config_path)
    val = ConfigParser.get(section, key)

    try:
        return int(val)
    except ValueError:
        pass

    try:
        return float(val)
    except ValueError:
        pass

    return val


def load_json(file_path: str) -> List[Dict]:
    """Load JSON data from a given file path."""
    with open(file_path, 'r') as f:
        return json.load(f)


def force_list(string_or_list: Union[str, List[str]]):
    """Force a string or list of strings to a list of strings."""
    if string_or_list is None:
        return []
    if isinstance(string_or_list, str):
        return [string_or_list]
    else:
        return string_or_list


def create_batches(
    items: List[str],
    batch_size: int
) -> List[List[str]]:
    """Split a list into smaller batches."""
    batches = []
    for i in range(0, len(items), batch_size):
        batches.append(items[i:i + batch_size])
    return batches


# =========================================================================== #

if __name__ == '__main__':
    pass
