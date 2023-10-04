from enum import Enum


# =========================================================================== #

class EnvType(Enum):
    DEV = 'Development'
    TST = 'Test'
    PRD = 'Production'


class SeedPosition(Enum):
    START = 'start'
    END = 'end'


class ConfigType(Enum):
    MAIN = 'config.ini'
    SECRETS = 'secrets.ini'


# =========================================================================== #

if __name__ == '__main__':
    pass