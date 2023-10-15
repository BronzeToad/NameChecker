import pytest

from src.utils.validator import InvalidConfigValueError

def test_validator_init(validator):
    assert validator.validator_type.name == 'CONFIG'

def test_get_error_type(validator):
    assert validator._get_error_type() == InvalidConfigValueError

def test_check_integer_not_value(validator):
    with pytest.raises(InvalidConfigValueError):
        validator._check_integer('Test Integer', None)

def test_check_integer_not_int(validator):
    with pytest.raises(InvalidConfigValueError):
        validator._check_integer('Test Integer', '1')

def test_check_string_not_value(validator):
    with pytest.raises(InvalidConfigValueError):
        validator._check_string('Test String', None)

def test_check_string_not_str(validator):
    with pytest.raises(InvalidConfigValueError):
        validator._check_string('Test String', 1)

# testing integer method
@pytest.mark.parametrize('value, min_value, max_value', [
        (None, None, None),
    ])
def test_integer_default(validator):
    validator.integer(1)

def test_integer_min(validator):
    validator.integer(1, min_value=1)

# testing directory method

# testing filename method

# testing url method

# testing api_token method
