import configparser
from enum import Enum
from typing import Optional, Union

from src.utils.toad_utils import find_project_root
from src.utils.validator import Validator, ValidatorType

# =============================================================================================== #

CONFIG_FILES = ['config.ini', 'secrets.ini']

class EnvType(Enum):
    DEV = 'Development'
    TST = 'Test'
    PRD = 'Production'


class ConfigHelper:
    def __init__(
        self,
        env_type: Union[EnvType, str],
        test_mode: Optional[bool] = False
    ) -> None:
        self.env_type = EnvType(env_type)
        self.test_mode = test_mode
        self._batch_size = None
        self._batch_retries = None
        self._seeds_filename = None
        self._results_filename = None
        self._godaddy_max_retries = None
        self._godaddy_api_url = None
        self._github_api_url = None
        self._godaddy_api_key = None
        self._godaddy_api_secret = None
        self._github_token = None
        self.config = configparser.ConfigParser()
        self.load_config_files()
        self.validator = Validator(ValidatorType.CONFIG)
        self.initialize_properties()


    def load_config_files(self) -> None:
        root_dir = find_project_root('NameChecker', self.test_mode)
        config_dir = root_dir / 'cfg'
        [self.config.read(config_dir / config_file) for config_file in CONFIG_FILES]

    def initialize_properties(self) -> None:
        self._batch_size = self.config.getint('Batch', 'BATCH_SIZE')
        self._batch_retries = self.config.getint('Batch', 'BATCH_RETRIES')
        self._seeds_filename = self.config.get('Filename', 'SEEDS')
        self._results_filename = self._results_filename_switch()
        self._godaddy_max_retries = self.config.getint('GoDaddy', 'MAX_RETRIES')
        self._godaddy_api_url = self._godaddy_api_url_switch()
        self._github_api_url = self.config.get('GitHub', 'BASE_API_URL')
        self._godaddy_api_key = self._godaddy_api_key_switch()
        self._godaddy_api_secret = self._godaddy_api_secret_switch()
        self._github_token = self.config.get('GitHub', 'TOKEN')
        
    def get_config_val(self, section: str, key: str) -> str:
        return self.config.get(section, key)

    @property
    def batch_size(self) -> int:
        return self._batch_size
    
    @batch_size.setter
    def batch_size(self, value: int) -> None:
        self.validator.integer(value, min_value=1)
        self._batch_size = value

    @property
    def batch_retries(self) -> int:
        return self._batch_retries
    
    @batch_retries.setter
    def batch_retries(self, value: int) -> None:
        self.validator.integer(value, min_value=0)
        self._batch_retries = value

    @property
    def seeds_filename(self) -> str:
        return self._seeds_filename
    
    @seeds_filename.setter
    def seeds_filename(self, value: str) -> None:
        self.validator.filename(value)
        self._seeds_filename = value

    @property
    def results_filename(self) -> str:
        return self._results_filename
    
    @results_filename.setter
    def results_filename(self, value: str) -> None:
        self.validator.filename(value)
        self._results_filename = value

    def _results_filename_switch(self) -> str:
        if self.env_type == EnvType.PRD:
            return self.config.get('Filename', 'RESULTS')
        else:
            return self.config.get('Filename', 'TST_RESULTS')

    @property
    def godaddy_max_retries(self) -> int:
        return self._godaddy_max_retries
    
    @godaddy_max_retries.setter
    def godaddy_max_retries(self, value: int) -> None:
        self.validator.integer(value, min_value=0)
        self._godaddy_max_retries = value

    @property
    def godaddy_api_url(self) -> str:
        return self._godaddy_api_url
    
    @godaddy_api_url.setter
    def godaddy_api_url(self, value: str) -> None:
        self.validator.url(value)
        self._godaddy_api_url = value

    def _godaddy_api_url_switch(self) -> str:
        if self.env_type == EnvType.PRD:
            return self.config.get('GoDaddy', 'PRD_API_URL')
        else:
            return self.config.get('GoDaddy', 'DEV_API_URL')

    @property
    def github_api_url(self) -> str:
        return self._github_api_url

    @github_api_url.setter
    def github_api_url(self, value: str) -> None:
        self.validator.url(value)
        self._github_api_url = value

    @property
    def godaddy_api_key(self) -> str:
        return self._godaddy_api_key

    @godaddy_api_key.setter
    def godaddy_api_key(self, value: str) -> None:
        self.validator.api_token(value)
        self._godaddy_api_key = value

    def _godaddy_api_key_switch(self) -> str:
        if self.env_type == EnvType.PRD:
            return self.config.get('GoDaddy', 'PRD_API_KEY')
        else:
            return self.config.get('GoDaddy', 'DEV_API_KEY')

    @property
    def godaddy_api_secret(self) -> str:
        return self._godaddy_api_secret
    
    @godaddy_api_secret.setter
    def godaddy_api_secret(self, value: str) -> None:
        self.validator.api_token(value)
        self._godaddy_api_secret = value

    def _godaddy_api_secret_switch(self) -> str:
        if self.env_type == EnvType.PRD:
            return self.config.get('GoDaddy', 'PRD_API_SECRET')
        else:
            return self.config.get('GoDaddy', 'DEV_API_SECRET')

    @property
    def github_token(self) -> str:
        return self._github_token
    
    @github_token.setter
    def github_token(self, value: str) -> None:
        self.validator.api_token(value, expected_prefix='github_pat_')
        self._github_token = value
