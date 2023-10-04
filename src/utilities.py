import configparser
import json
import os

from typing import Dict, List, Optional, Union
from src.enum_factory import ConfigType, EnvType


# =========================================================================== #



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


def get_results_filepath(env_type: EnvType) -> str:
    output_dir = get_config_val('Directories', 'OUTPUT')

    if env_type == EnvType.PRD:
        return os.path.join(output_dir, 'results.json')
    else:
        return os.path.join(output_dir, 'test_results.json')


def get_batch_size() -> int:
    return get_config_val('Main', 'BATCH_SIZE')


def get_max_retries() -> int:
    return Utils.get_config_val('Main', 'MAX_RETRIES')


def get_name_seeds(seed_position: SeedPosition) -> List[str]:
    config_path = Utils.get_config_val('Directories', 'SEEDS')
    seeds = Utils.load_json(config_path)
    for seed in seeds:
        if seed['seedPosition'] == seed_position.value:
            return seed['seedItems']
# =========================================================================== #

if __name__ == '__main__':
    pass

