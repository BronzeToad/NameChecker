import configparser
import os
from typing import Optional, Union
from pathlib import Path

from src.enum_factory import ConfigType, EnvType
from warnings import warn

# =========================================================================== #

class ConfigHelper:

    def __init__(self):
        self.__post_init__()


    def __post_init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.secrets = configparser.ConfigParser()
        self.secrets.read('secrets.ini')


    def get_config_val(self, section: str, key: str):
        return self.clean_returned_val(self.config.get(section, key))


    def get_secret_val(self, section: str, key: str):
        return self.clean_returned_val(self.secrets.get(section, key))


    @staticmethod
    def clean_returned_val(val: str) -> Union[str, int, float]:
        if val == '':
            return None

        try:
            return int(val)
        except ValueError:
            pass

        try:
            return float(val)
        except ValueError:
            pass

        return val


    def get_batch_size(self) -> int:
        return self.get_config_val('Batch', 'BATCH_SIZE')

    def get_batch_retries(self) -> int:
        return self.get_config_val('Batch', 'BATCH_RETRIES')


    def get_root_dir(self) -> str:
        return self.get_config_val('Directory', 'ROOT')

    def get_config_dir(self) -> str:
        return self.get_config_val('Directory', 'CONFIG')

    def get_output_dir(self) -> str:
        return self.get_config_val('Directory', 'OUTPUT')


    def get_seeds_filename(self) -> str:
        return self.get_config_val('Filename', 'SEEDS')

    def get_results_filename(self, env_type: EnvType) -> str:
        if env_type == EnvType.PRD:
            return self.get_config_val('Filename', 'RESULTS')
        else:
            return self.get_config_val('Filename', 'TST_RESULTS')


    def get_godaddy_api_url(self, env_type: EnvType) -> str:
        if env_type == EnvType.PRD:
            return self.get_config_val('GoDaddy', 'PRD_API_URL')
        else:
            if env_type == EnvType.TST:
                warn('No API URL found for test environment. '
                     'Using API URL for development environment...')
            return self.get_config_val('GoDaddy', 'DEV_API_URL')

    def get_godaddy_max_retries(self) -> int:
        return self.get_config_val('GoDaddy', 'MAX_RETRIES')


    def get_github_api_url(self) -> str:
        return self.get_config_val('GitHub', 'BASE_API_URL')


    def get_godaddy_api_key(self, env_type: EnvType) -> str:
        if env_type == EnvType.PRD:
            return self.get_secret_val('GoDaddy', 'PRD_API_KEY')
        else:
            if env_type == EnvType.TST:
                warn('No API key found for test environment. '
                     'Using API key for development environment...')
            return self.get_secret_val('GoDaddy', 'DEV_API_KEY')

    def get_godaddy_api_secret(self, env_type: EnvType) -> str:
        if env_type == EnvType.PRD:
            return self.get_secret_val('GoDaddy', 'PRD_API_SECRET')
        else:
            if env_type == EnvType.TST:
                warn('No API secret found for test environment. Using API secret for development environment...')
            return self.get_secret_val('GoDaddy', 'DEV_API_SECRET')


# =========================================================================== #

if __name__ == '__main__':
    from icecream import ic

    cfg = ConfigHelper()

    ic(cfg.get_batch_size())
    ic(cfg.get_batch_retries())
    ic(cfg.get_root_dir())
    ic(cfg.get_config_dir())
    ic(cfg.get_output_dir())
    ic(cfg.get_seeds_filename())
    ic(cfg.get_results_filename(EnvType.PRD))
    ic(cfg.get_results_filename(EnvType.TST))
    ic(cfg.get_godaddy_api_url(EnvType.DEV))
    ic(cfg.get_godaddy_api_url(EnvType.TST))
    ic(cfg.get_godaddy_api_url(EnvType.PRD))
    ic(cfg.get_godaddy_max_retries())
    ic(cfg.get_github_api_url())
    ic(cfg.get_godaddy_api_key(EnvType.DEV))
    ic(cfg.get_godaddy_api_key(EnvType.TST))
    ic(cfg.get_godaddy_api_key(EnvType.PRD))
    ic(cfg.get_godaddy_api_secret(EnvType.DEV))
    ic(cfg.get_godaddy_api_secret(EnvType.TST))
    ic(cfg.get_godaddy_api_secret(EnvType.PRD))
