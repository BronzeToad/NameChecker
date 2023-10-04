import json
import os
from enum import Enum
from typing import Dict, List, Optional, Union

import src.utilities as Utils


# =========================================================================== #

class EnvType(Enum):
    DEV = 'Development'
    TST = 'Test'
    PRD = 'Production'


class SeedPosition(Enum):
    START = 'start'
    END = 'end'


# =========================================================================== #

class NameChecker:

    def __init__(
        self,
        env_type: EnvType,
        names: Optional[List[str]] = None,
        batch_size: Optional[int] = None,
        max_retries: Optional[int] = None
    ):
        self.env_type = env_type
        self.names = names
        self.batch_size = batch_size
        self.max_retries = max_retries
        self.__post_init__()


    def __post_init__(self):
        self.names = Utils.force_list(self.names) or self.get_names()
        self.batch_size = self.batch_size or self.get_batch_size()
        self.max_retries = self.max_retries or self.get_max_retries()
        self.results_filepath = self.get_results_filepath()


    @staticmethod
    def get_batch_size() -> int:
        return Utils.get_config_val('Main', 'BATCH_SIZE')


    @staticmethod
    def get_max_retries() -> int:
        return Utils.get_config_val('Main', 'MAX_RETRIES')


    @staticmethod
    def get_name_seeds(seed_position: SeedPosition) -> List[str]:
        config_path = Utils.get_config_val('Directories', 'SEEDS')
        seeds = Utils.load_json(config_path)
        for seed in seeds:
            if seed['seedPosition'] == seed_position.value:
                return seed['seedItems']


    def get_names(self) -> List[str]:
        names = []
        for start in self.get_name_seeds(SeedPosition.START):
            for end in self.get_name_seeds(SeedPosition.END):
                if start != end:
                    names.append(start + end)
        return names


    def get_results_filepath(self) -> str:
        root = Utils.get_config_val('Directories', 'ROOT')

        if self.env_type == EnvType.PRD:
            return os.path.join(root, 'output', 'results.json')
        else:
            return os.path.join(root, 'output', 'test_results.json')


    def save_results(self, results: List[Dict[str, Union[str, bool]]]):
        try:
            with open(self.results_filepath, 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []

        for item in results:
            for existing_item in existing_data:
                if item['name'] == existing_item['name']:
                    existing_item.update(item)
                    break
            else:
                existing_data.append(item)

        with open(self.results_filepath, 'w') as f:
            json.dump(existing_data, f, indent=4)


# =========================================================================== #

if __name__ == '__main__':
    checker = NameChecker(env_type=EnvType.DEV)
    from icecream import ic
    ic(checker.env_type)
    ic(checker.names[:10])
    ic(checker.batch_size)
    ic(checker.max_retries)
