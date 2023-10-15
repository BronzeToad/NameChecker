import configparser
import os
from enum import Enum
import re
from typing import Union
from src.utils.validator import Validator, ValidatorType

# =============================================================================================== #

CONFIG_FILES = ['config.ini', 'secrets.ini']

class EnvType(Enum):
    DEV = 'Development'
    TST = 'Test'
    PRD = 'Production'

class InvalidConfigValueError(ValueError):
    """Raised when an invalid configuration value is provided."""


class ConfigHelper:
    def __init__(self, env_type: Union[EnvType, str]) -> None:
        print("Initializing ConfigHelper...")
        self.env_type = EnvType(env_type)
        self.config = configparser.ConfigParser()
        self.load_config_files()
        self.validator = Validator(ValidatorType.CONFIG)
        self.initialize_properties()


    def load_config_files(self) -> None:
        print("Loading config files...")
        config_dir = os.path.dirname(os.path.abspath(__file__))
        for config_file in CONFIG_FILES:
            config_filepath = os.path.join(config_dir, config_file)
            self.config.read(config_filepath)

    def initialize_properties(self) -> None:
        print("Initializing properties...")
        self._batch_size = self.config.getint('Batch', 'BATCH_SIZE', fallback=1)
        self._batch_retries = self.config.getint('Batch', 'BATCH_RETRIES', fallback=0)
        self._root_dir = self.config.get('Directory', 'ROOT')
        self._config_dir = self.config.get('Directory', 'CONFIG')
        self._output_dir = self.config.get('Directory', 'OUTPUT')
        self._seeds_filename = self.config.get('Filename', 'SEEDS')
        self._results_filename = self._results_filename_switch()
        self._godaddy_max_retries = self.config.getint('GoDaddy', 'MAX_RETRIES', fallback=0)
        self._godaddy_api_url = self._godaddy_api_url_switch()
        self._github_api_url = self.config.get('GitHub', 'BASE_API_URL')
        self._godaddy_api_key = self._godaddy_api_key_switch()
        self._godaddy_api_secret = self._godaddy_api_secret_switch()
        self._github_token = self.config.get('GitHub', 'TOKEN')
        
    def get_config_val(self, section: str, key: str) -> str:
        return self.config.get(section, key)

    @property
    def batch_size(self) -> int:
        print("Accessing batch_size property...")
        return self._batch_size
    
    @batch_size.setter
    def batch_size(self, value: int) -> None:
        print("Setting batch_size property...")
        self.validator.integer(value, min_value=1)
        self._batch_size = value

    @property
    def batch_retries(self) -> int:
        print("Accessing batch_retries property...")
        return self._batch_retries
    
    @batch_retries.setter
    def batch_retries(self, value: int) -> None:
        print("Setting batch_retries property...")
        self.validator.integer(value, min_value=0)
        self._batch_retries = value

    @property
    def root_dir(self) -> str:
        print("Accessing root_dir property...")
        return self._root_dir
    
    @root_dir.setter
    def root_dir(self, value: str) -> None:
        print("Setting root_dir property...")
        self.validator.directory(value)
        self._root_dir = value
    
    @property
    def config_dir(self) -> str:
        print("Accessing config_dir property...")
        return self._config_dir
    
    @config_dir.setter
    def config_dir(self, value: str) -> None:
        self.validator.directory(value)
        self._config_dir = value

    @property
    def output_dir(self) -> str:
        print("Accessing output_dir property...")
        return self._output_dir
    
    @output_dir.setter
    def output_dir(self, value: str) -> None:
        print("Setting output_dir property...")
        self.validator.directory(value)
        self._output_dir = value

    @property
    def seeds_filename(self) -> str:
        print("Accessing seeds_filename property...")
        return self._seeds_filename
    
    @seeds_filename.setter
    def seeds_filename(self, value: str) -> None:
        print("Setting seeds_filename property...")
        self.validator.filename(value)
        self._seeds_filename = value

    @property
    def results_filename(self) -> str:
        print("Accessing results_filename property...")
        return self._results_filename
    
    @results_filename.setter
    def results_filename(self, value: str) -> None:
        print("Setting results_filename property...")
        self.validator.filename(value)
        self._results_filename = value

    def _results_filename_switch(self) -> str:
        if self.env_type == EnvType.PRD:
            return self.config.get('Filename', 'RESULTS')
        else:
            return self.config.get('Filename', 'TST_RESULTS')

    @property
    def godaddy_max_retries(self) -> int:
        print("Accessing godaddy_max_retries property...")
        return self._godaddy_max_retries
    
    @godaddy_max_retries.setter
    def godaddy_max_retries(self, value: int) -> None:
        print("Setting godaddy_max_retries property...")
        self.validator.integer(value, min_value=0)
        self._godaddy_max_retries = value

    @property
    def godaddy_api_url(self) -> str:
        print("Accessing godaddy_api_url property...")
        return self._godaddy_api_url
    
    @godaddy_api_url.setter
    def godaddy_api_url(self, value: str) -> None:
        print("Setting godaddy_api_url property...")
        self.validator.url(value)
        self._godaddy_api_url = value

    def _godaddy_api_url_switch(self) -> str:
        if self.env_type == EnvType.PRD:
            return self.config.get('GoDaddy', 'PRD_API_URL')
        else:
            return self.config.get('GoDaddy', 'DEV_API_URL')

    @property
    def github_api_url(self) -> str:
        print("Accessing github_api_url property...")
        return self._github_api_url
    
    @github_api_url.setter
    def github_api_url(self, value: str) -> None:
        print("Setting github_api_url property...")
        self.validator.url(value)
        self._github_api_url = value

    @property
    def godaddy_api_key(self) -> str:
        print("Accessing godaddy_api_key property...")
        return self._godaddy_api_key

    @godaddy_api_key.setter
    def godaddy_api_key(self, value: str) -> None:
        print("Setting godaddy_api_key property...")
        self.validator.api_token(value)
        self._godaddy_api_key = value

    def _godaddy_api_key_switch(self) -> str:
        if self.env_type == EnvType.PRD:
            return self.config.get('GoDaddy', 'PRD_API_KEY')
        else:
            return self.config.get('GoDaddy', 'DEV_API_KEY')

    @property
    def godaddy_api_secret(self) -> str:
        print("Accessing godaddy_api_secret property...")
        return self._godaddy_api_secret
    
    @godaddy_api_secret.setter
    def godaddy_api_secret(self, value: str) -> None:
        print("Setting godaddy_api_secret property...")
        self.validator.api_token(value)
        self._godaddy_api_secret = value

    def _godaddy_api_secret_switch(self) -> str:
        if self.env_type == EnvType.PRD:
            return self.config.get('GoDaddy', 'PRD_API_SECRET')
        else:
            return self.config.get('GoDaddy', 'DEV_API_SECRET')

    @property
    def github_token(self) -> str:
        print("Accessing github_token property...")
        return self._github_token
    
    @github_token.setter
    def github_token(self, value: str) -> None:
        print("Setting github_token property...")
        self.validator.api_token(value, expected_prefix='github_pat_')
        self._github_token = value
    