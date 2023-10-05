import configparser
import os
from typing import Union
from warnings import warn
from dataclasses import dataclass, field
from src.enum_factory import EnvType


# =============================================================================================== #

@dataclass
class ConfigHelper:
    env_type: EnvType
    config: configparser.ConfigParser = field(init=False, repr=False)
    secrets: configparser.ConfigParser = field(init=False, repr=False)
    batch_size: int = field(init=False, repr=False)
    batch_retries: int = field(init=False, repr=False)
    root_dir: str = field(init=False, repr=False)
    config_dir: str = field(init=False, repr=False)
    output_dir: str = field(init=False, repr=False)
    seeds_filename: str = field(init=False, repr=False)
    results_filename: str = field(init=False, repr=False)
    godaddy_api_url: str = field(init=False, repr=False)
    godaddy_max_retries: int = field(init=False, repr=False)
    godaddy_api_key: str = field(init=False, repr=False)
    godaddy_api_secret: str = field(init=False, repr=False)
    github_api_url: str = field(init=False, repr=False)
    github_token: str = field(init=False, repr=False)


    def __post_init__(self):
        self.set_config_parsers()
        self.set_batch_config_vals()
        self.set_dir_config_vals()
        self.set_filename_config_vals()
        self.set_godaddy_config_vals()
        self.set_github_config_vals()


    def set_config_parsers(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, 'config.ini')
        secrets_path = os.path.join(current_dir, 'secrets.ini')

        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        self.secrets = configparser.ConfigParser()
        self.secrets.read(secrets_path)


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


    def set_batch_config_vals(self):
        self.batch_size = self.get_config_val('Batch', 'BATCH_SIZE')
        self.batch_retries = self.get_config_val('Batch', 'BATCH_RETRIES')

    def set_dir_config_vals(self):
        self.root_dir = self.get_config_val('Directory', 'ROOT')
        self.config_dir = self.get_config_val('Directory', 'CONFIG')
        self.output_dir = self.get_config_val('Directory', 'OUTPUT')

    def set_filename_config_vals(self):
        self.seeds_filename = self.get_config_val('Filename', 'SEEDS')
        if self.env_type == EnvType.PRD:
            self.results_filename = self.get_config_val('Filename', 'RESULTS')
        else:
            self.results_filename = self.get_config_val('Filename', 'TST_RESULTS')

    def set_godaddy_config_vals(self):
        self.godaddy_max_retries = self.get_config_val('GoDaddy', 'MAX_RETRIES')
        if self.env_type == EnvType.PRD:
            self.godaddy_api_url = self.get_config_val('GoDaddy', 'PRD_API_URL')
            self.godaddy_api_key = self.get_secret_val('GoDaddy', 'PRD_API_KEY')
            self.godaddy_api_secret = self.get_secret_val('GoDaddy', 'PRD_API_SECRET')
        else:
            if self.env_type == EnvType.TST:
                warn('No config values found for test environment. '
                     'Using values for development environment...')
                self.godaddy_api_url = self.get_config_val('GoDaddy', 'DEV_API_URL')
                self.godaddy_api_key = self.get_secret_val('GoDaddy', 'DEV_API_KEY')
                self.godaddy_api_secret = self.get_secret_val('GoDaddy', 'DEV_API_SECRET')

    def set_github_config_vals(self):
        self.github_api_url = self.get_config_val('GitHub', 'BASE_API_URL')
        self.github_token = self.get_secret_val('GitHub', 'TOKEN')


# =============================================================================================== #

if __name__ == '__main__':
    from icecream import ic

    cfg = ConfigHelper(EnvType.PRD)

    ic(cfg.batch_size)
    ic(cfg.batch_retries)
    ic(cfg.root_dir)
    ic(cfg.config_dir)
    ic(cfg.output_dir)
    ic(cfg.seeds_filename)
    ic(cfg.results_filename)
    ic(cfg.godaddy_api_url)
    ic(cfg.godaddy_max_retries)
    ic(cfg.godaddy_api_key)
    ic(cfg.godaddy_api_secret)
    ic(cfg.github_api_url)
    ic(cfg.github_token)
