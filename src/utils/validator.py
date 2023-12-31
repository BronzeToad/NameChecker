import os
from enum import Enum, auto
from pathlib import Path
from typing import List, Optional, Type, Union
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


    def _check_integer(self, error_msg_base: str, value: int) -> bool:
        if value is None:
            raise self.error_type(f"{error_msg_base} cannot be None.")
        if not isinstance(value, int):
            raise self.error_type(f"{error_msg_base} must be an integer.")
        return True


    def _check_string(self, error_msg_base: str, value: str) -> bool:
        """Validates that the provided value is a string."""
        if value is None:
            raise self.error_type(f"{error_msg_base} cannot be None.")
        if value == '':
            raise self.error_type(f"{error_msg_base} cannot be empty.")
        if not isinstance(value, str):
            raise self.error_type(f"{error_msg_base} must be a string.")
        return True


    def integer(
        self,
        value: int,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None
    ) -> bool:
        """Validates that the provided value is an integer."""
        error_msg_base = f"Value {value} is invalid: number value"
        if self._check_integer(error_msg_base, value):
            if None not in (min_value, max_value) and min_value > max_value:
                raise self.error_type(f"{error_msg_base} min_value cannot be greater than max_value.")
            if min_value is not None and value < min_value:
                raise self.error_type(f"{error_msg_base} must be {min_value} or greater.")
            if max_value is not None and value > max_value:
                raise self.error_type(f"{error_msg_base} must be {max_value} or less.")
        return True


    def directory(
        self,
        value: Union[str, Path],
        check_absolute_path: Optional[bool] = True,
        check_exists: Optional[bool] = True,
        check_is_dir: Optional[bool] = True,
    ) -> bool:
        """Validates a directory path."""
        error_msg_base = f"Directory {value} is invalid: directory"
        if value is None:
            raise self.error_type(f"{error_msg_base} cannot be None.")
        if value == '':
            raise self.error_type(f"{error_msg_base} cannot be empty.")
        if not isinstance(value, str) and not isinstance(value, Path):
            raise self.error_type(f"{error_msg_base} must be a string or Path.")
        str_val = value.as_posix() if isinstance(value, Path) else value
        if check_absolute_path and not os.path.isabs(str_val):
            raise self.error_type(f"{error_msg_base} must be an absolute path.")
        if check_exists and not os.path.exists(str_val):
            raise self.error_type(f"{error_msg_base} does not exist.")
        if check_is_dir and not os.path.isdir(str_val):
            raise self.error_type(f"{error_msg_base} is not a directory.")
        return True


    def filename(
        self,
        value: str,
        invalid_chars=None,
        check_path_seq: Optional[bool] = True,
    ) -> bool:
        """Validates a filename."""
        if invalid_chars is None:
            invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        error_msg_base = f"Filename {value} is invalid: filename"
        if self._check_string(error_msg_base, value):
            if invalid_chars is not None and any(char in value for char in invalid_chars):
                raise self.error_type(f"{error_msg_base} contains one or more invalid characters.")
            if check_path_seq and ".." in value:
                raise self.error_type(f"{error_msg_base} contains a potentially unsafe path sequence.")
        return True


    def url(
        self,
        value: str,
        check_scheme: Optional[bool] = True,
        check_domain: Optional[bool] = True,
    ) -> bool:
        error_msg_base = f"URL {value} is invalid: URL"
        if self._check_string(error_msg_base, value):
            url = urlparse(value)
            if check_scheme:
                if not url.scheme or url.scheme not in ['http', 'https']:
                    raise self.error_type(f"{error_msg_base} must have a valid scheme.")
            if check_domain and not url.netloc:
                raise self.error_type(f"{error_msg_base} must have a valid domain.")
        return True


    def api_token(
        self,
        value: str,
        expected_length: Optional[int] = None,
        expected_prefix: Optional[str] = None,
        expected_suffix: Optional[str] = None,
        invalid_chars: Optional[List[str]] = None
    ) -> bool:
        error_msg_base = f"API token {value} is invalid: API token"
        if self._check_string(error_msg_base, value):
            if expected_length is not None and len(value) != expected_length:
                raise self.error_type(f"{error_msg_base} must be {expected_length} characters.")
            if expected_prefix is not None and not value.startswith(expected_prefix):
                raise self.error_type(f"{error_msg_base} must start with {expected_prefix}.")
            if expected_suffix is not None and not value.endswith(expected_suffix):
                raise self.error_type(f"{error_msg_base} must end with {expected_suffix}.")
            if invalid_chars is not None and any(char in value for char in invalid_chars):
                raise self.error_type(f"{error_msg_base} contains one or more invalid characters.")
        return True
