import configparser
from dbm import error
from ftplib import error_perm
import os
from enum import Enum, auto
from typing import Union, Optional, Type, List
from urllib.parse import urlparse


# =============================================================================================== #

class ValidatorType(Enum):
    CONFIG = auto()


class InvalidConfigValueError(ValueError):
    """Raised when an invalid configuration value is provided."""


class Validator:

    def __init__(self, validator_type: Union[ValidatorType, str]) -> None:
        self.validator_type = ValidatorType(validator_type)
        self.error_type = self._get_error_type()


    def _get_error_type(self) -> Type[Exception]:
        """Get the error type to raise."""
        error_type_map = {
            ValidatorType.CONFIG: InvalidConfigValueError,
        }
        if self.validator_type in error_type_map:
            return error_type_map[self.validator_type]
        else:
            raise ValueError(f"Invalid validator type: {self.validator_type}")


    def _check_integer(self, error_msg_base: str, value: int) -> None:
        if not value:
            raise self.error_type(f"{error_msg_base} cannot be empty.")
        if not isinstance(value, int):
            raise self.error_type(f"{error_msg_base} must be an integer.")


    def _check_string(self, error_msg_base: str, value: str) -> None:
        """Validates that the provided value is a string."""
        if not value:
            raise self.error_type(f"{error_msg_base} cannot be empty.")
        if not isinstance(value, str):
            raise self.error_type(f"{error_msg_base} must be a string.")


    def integer(
        self,
        value: int,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None
    ) -> None:
        """Validates that the provided value is an integer."""
        error_msg_base = f"Value {value} is invalid: number value"
        self._check_integer(error_msg_base, value)
        if min_value and value < min_value:
            raise self.error_type(f"{error_msg_base} must be {min_value} or greater.")
        if max_value and value > max_value:
            raise self.error_type(f"{error_msg_base} must be {max_value} or less.")


    def directory(
        self,
        dir_path: str,
        check_absolute_path: Optional[bool] = True,
        check_exists: Optional[bool] = True,
        check_is_dir: Optional[bool] = True,
    ) -> None:
        """Validates a directory path."""
        error_msg_base = f"Directory {dir_path} is invalid: directory"
        self._check_string(error_msg_base, dir_path)
        if check_absolute_path and not os.path.isabs(dir_path):
            raise self.error_type(f"{error_msg_base} must be an absolute path.")
        if check_exists and not os.path.exists(dir_path):
            raise self.error_type(f"{error_msg_base} does not exist.")
        if check_is_dir and not os.path.isdir(dir_path):
            raise self.error_type(f"{error_msg_base} is not a directory.")


    def filename(
        self,
        filename: str,
        invalid_chars=None,
        check_path_seq: Optional[bool] = True,
    ) -> None:
        """Validates a filename."""
        if invalid_chars is None:
            invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        error_msg_base = f"Filename {filename} is invalid: filename"
        self._check_string(error_msg_base, filename)
        if invalid_chars and any(char in filename for char in invalid_chars):
            raise self.error_type(f"{error_msg_base} contains one or more invalid characters.")
        if check_path_seq and ".." in filename:
            raise self.error_type(f"{error_msg_base} contains a potentially unsafe path sequence.")


    def url(
        self,
        url: str,
        check_schema: Optional[bool] = True,
        check_domain: Optional[bool] = True,
    ) -> None:
        error_msg_base = f"URL {url} is invalid: URL"
        self._check_string(error_msg_base, url)
        parsed_url = urlparse(url)
        if check_schema:
            if not parsed_url.scheme or parsed_url.scheme not in ['http', 'https']:
                raise self.error_type(f"{error_msg_base} must have a valid scheme.")
        if check_domain and not parsed_url.netloc:
            raise self.error_type(f"{error_msg_base} must have a valid domain.")


    def api_token(
        self,
        token_value: str,
        expected_length: Optional[int] = None,
        expected_prefix: Optional[str] = None,
        expected_suffix: Optional[str] = None,
        invalid_chars: Optional[List[str]] = None
    ) -> None:
        error_msg_base = f"API token {token_value} is invalid: API token"
        self._check_string(error_msg_base, token_value)
        if expected_length and len(token_value) != expected_length:
            raise self.error_type(f"{error_msg_base} must be {expected_length} characters.")
        if expected_prefix and not token_value.startswith(expected_prefix):
            raise self.error_type(f"{error_msg_base} must start with {expected_prefix}.")
        if expected_suffix and not token_value.endswith(expected_suffix):
            raise self.error_type(f"{error_msg_base} must end with {expected_suffix}.")
        if invalid_chars and any(char in token_value for char in invalid_chars):
            raise self.error_type(f"{error_msg_base} contains one or more invalid characters.")