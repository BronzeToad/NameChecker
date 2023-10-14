import configparser
import os
from enum import Enum
from typing import Union

# =============================================================================================== #

class EnvType(Enum):
    DEV = 'Development'
    TST = 'Test'
    PRD = 'Production'

CONFIG_FILES = ['config.ini', 'secrets.ini']


class ConfigHelper:
    def __init__(self, env_type: Union[EnvType, str]) -> None:
        print("Initializing ConfigHelper...")
        self.env_type = EnvType(env_type)
        self.__post_init__()
        self._batch_size = None
        self._batch_retries = None
        self._root_dir = None
        self._config_dir = None
        self._output_dir = None
        self._seeds_filename = None
        self._results_filename = None
        self._godaddy_max_retries = None
        self._godaddy_api_url = None
        self._godaddy_api_key = None
        self._godaddy_api_secret = None
        self._github_api_url = None
        self._github_token = None


    def __post_init__(self) -> None:
        print("Executing post init...")
        self.config = configparser.ConfigParser()
        self.load_config_files()


    def load_config_files(self) -> None:
        print("Loading config files...")
        config_dir = os.path.dirname(os.path.abspath(__file__))
        for config_file in CONFIG_FILES:
            config_filepath = os.path.join(config_dir, config_file)
            self.config.read(config_filepath)

    
    def get_config_val(self, section: str, key: str) -> str:
        return self.config.get(section, key)


    @property
    def batch_size(self) -> int:
        print("Accessing batch_size property...")
        if self._batch_size is None:
            self._batch_size = self.config.getint('Batch', 'BATCH_SIZE')
        return self._batch_size
    
    @batch_size.setter
    def batch_size(self, value: int) -> None:
        self._batch_size = value

    @property
    def batch_retries(self) -> int:
        if self._batch_retries is None:
            self._batch_retries = self.config.getint('Batch', 'BATCH_RETRIES')
        return self._batch_retries
    
    @batch_retries.setter
    def batch_retries(self, value: int) -> None:
        self._batch_retries = value

    @property
    def root_dir(self) -> str:
        if self._root_dir is None:
            self._root_dir = self.config.get('Directory', 'ROOT')
        return self._root_dir
    
    @property
    def config_dir(self) -> str:
        if self._config_dir is None:
            self._config_dir = self.config.get('Directory', 'CONFIG')
        return self._config_dir
    
    @property
    def output_dir(self) -> str:
        if self._output_dir is None:
            self._output_dir = self.config.get('Directory', 'OUTPUT')
        return self._output_dir

    @property
    def seeds_filename(self) -> str:
        if self._seeds_filename is None:
            self._seeds_filename = self.config.get('Filename', 'SEEDS')
        return self._seeds_filename
    
    @property
    def results_filename(self) -> str:
        if self._results_filename is None:
            if self.env_type == EnvType.PRD:
                self._results_filename = self.config.get('Filename', 'RESULTS')
            else:
                self._results_filename = self.config.get('Filename', 'TST_RESULTS')
        return self._results_filename

    @property
    def godaddy_max_retries(self) -> int:
        if self._godaddy_max_retries is None:
            self._godaddy_max_retries = self.config.getint('GoDaddy', 'MAX_RETRIES')
        return self._godaddy_max_retries
    
    @godaddy_max_retries.setter
    def godaddy_max_retries(self, value: int) -> None:
        self._godaddy_max_retries = value

    @property
    def godaddy_api_url(self) -> str:
        if self._godaddy_api_url is None:
            if self.env_type == EnvType.PRD:
                self._godaddy_api_url = self.config.get('GoDaddy', 'PRD_API_URL')
            else:
                self._godaddy_api_url = self.config.get('GoDaddy', 'DEV_API_URL')
        return self._godaddy_api_url
    
    @property
    def github_api_url(self) -> str:
        if self._github_api_url is None:
            self._github_api_url = self.config.get('GitHub', 'BASE_API_URL')
        return self._github_api_url
    
    @property
    def godaddy_api_key(self) -> str:
        if self._godaddy_api_key is None:
            if self.env_type == EnvType.PRD:
                self._godaddy_api_key = self.config.get('GoDaddy', 'PRD_API_KEY')
            else:
                self._godaddy_api_key = self.config.get('GoDaddy', 'DEV_API_KEY')
        return self._godaddy_api_key
    
    @property
    def godaddy_api_secret(self) -> str:
        if self._godaddy_api_secret is None:
            if self.env_type == EnvType.PRD:
                self._godaddy_api_secret = self.config.get('GoDaddy', 'PRD_API_SECRET')
            else:
                self._godaddy_api_secret = self.config.get('GoDaddy', 'DEV_API_SECRET')
        return self._godaddy_api_secret
    
    @property
    def github_token(self) -> str:
        if self._github_token is None:
            self._github_token = self.config.get('GitHub', 'GITHUB_TOKEN')
        return self._github_token
