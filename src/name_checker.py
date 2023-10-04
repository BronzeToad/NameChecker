from enum import Enum, auto
from typing import Dict, List, Optional, Union


# =========================================================================== #

class EnvType(Enum):
    DEV = auto()
    TST = auto()
    PRD = auto()


class ConfigType(Enum):
    MAIN = 'config.ini'
    SECRETS = 'secrets.ini'

# =========================================================================== #

class NameChecker:

    def __init__(
        self,
        env_type: EnvType,
        item_list_keys: Optional[Union[List[str], str]] = None
    ):
        self.env_type = env_type
        self.item_list_keys = item_list_keys
        self.__post_init__()

# =========================================================================== #

if __name__ == '__main__':
    pass