import pytest

from src.utils.validator import InvalidConfigValueError

def test_validator_init(validator):
    assert validator.validator_type.name == 'CONFIG'

def test_get_error_type(validator):
    assert validator._get_error_type() == InvalidConfigValueError


# testing _check_integer method
def test_check_integer_is_int(validator):
    assert validator._check_integer('Test Integer', 1) is True

def test_check_integer_none_value(validator):
    with pytest.raises(InvalidConfigValueError, match='cannot be empty'):
        validator._check_integer('Test Integer', None)

def test_check_integer_not_int(validator):
    with pytest.raises(InvalidConfigValueError, match='must be an integer'):
        validator._check_integer('Test Integer', '1')


# testing _check_string method
def test_check_string_is_str(validator):
    assert validator._check_string('Test String', 'test') is True

def test_check_string_none_value(validator):
    with pytest.raises(InvalidConfigValueError, match='cannot be empty'):
        validator._check_string('Test String', None)

def test_check_string_not_str(validator):
    with pytest.raises(InvalidConfigValueError, match='must be a string'):
        validator._check_string('Test String', 1)


# testing integer method
def test_integer_integer_value(validator):
    assert validator.integer(1) is True

def test_integer_none_value(validator):
    with pytest.raises(InvalidConfigValueError, match='cannot be empty'):
        validator.integer(None)

def test_integer_non_integer_value(validator):
    with pytest.raises(InvalidConfigValueError, match='must be an integer'):
        validator.integer('zero')

def test_integer_within_range(validator):
    assert validator.integer(5, min_value=1, max_value=10) is True

def test_integer_below_min_value(validator):
    with pytest.raises(InvalidConfigValueError, match='must be 1 or greater'):
        validator.integer(0, min_value=1, max_value=10)

def test_integer_above_max_value(validator):
    with pytest.raises(InvalidConfigValueError, match='must be 10 or less'):
        validator.integer(11, min_value=1, max_value=10)

def test_integer_only_min_value_set_below(validator):
    with pytest.raises(InvalidConfigValueError, match='must be 1 or greater'):
        validator.integer(0, min_value=1)

def test_integer_only_max_value_set_above(validator):
    with pytest.raises(InvalidConfigValueError, match='must be 10 or less'):
        validator.integer(11, max_value=10)


# testing directory method
# TODO


# testing filename method
# TODO


# testing url method
# TODO


# testing api_token method
# TODO
