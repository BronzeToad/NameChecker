import pytest

from src.utils.validator import InvalidConfigValueError

def test_validator_init(validator):
    assert validator.validator_type.name == 'CONFIG'

def test_get_error_type(validator):
    assert validator._get_error_type() == InvalidConfigValueError


# testing _check_integer method
def test_check_integer_valid(validator):
    assert validator._check_integer('Test Integer', 1) is True

def test_check_integer_value_none(validator):
    with pytest.raises(InvalidConfigValueError, match='cannot be None'):
        validator._check_integer('Test Integer', None)

def test_check_integer_bad_type(validator):
    with pytest.raises(InvalidConfigValueError, match='must be an integer'):
        validator._check_integer('Test Integer', '1')


# testing _check_string method
def test_check_string_valid(validator):
    assert validator._check_string('Test String', 'test') is True

def test_check_string_value_none(validator):
    with pytest.raises(InvalidConfigValueError, match='cannot be None'):
        validator._check_string('Test String', None)

def test_check_string_value_empty(validator):
    with pytest.raises(InvalidConfigValueError, match='cannot be empty'):
        validator._check_string('Test String', '')

def test_check_string_bad_type(validator):
    with pytest.raises(InvalidConfigValueError, match='must be a string'):
        validator._check_string('Test String', 1)


# testing integer method
def test_integer_value_valid(validator):
    assert validator.integer(1) is True

def test_integer_value_none(validator):
    with pytest.raises(InvalidConfigValueError, match='cannot be None'):
        validator.integer(None)

def test_integer_value_bad_type(validator):
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

def test_integer_at_min_boundary(validator):
    assert validator.integer(1, min_value=1, max_value=10) is True

def test_integer_at_max_boundary(validator):
    assert validator.integer(10, min_value=1, max_value=10) is True

def test_invalid_min_max_configuration(validator):
    with pytest.raises(InvalidConfigValueError, match='min_value cannot be greater than max_value'):
        validator.integer(5, min_value=10, max_value=1)

def test_negative_integer_value(validator):
    assert validator.integer(-5, min_value=-10, max_value=0) is True


# testing directory method
def test_directory_value_valid_path(validator, project_root):
    assert validator.directory(project_root) is True

def test_directory_value_valid_str(validator, project_root):
    assert validator.directory(project_root.as_posix()) is True

def test_directory_value_none(validator):
    with pytest.raises(InvalidConfigValueError, match='cannot be None'):
        validator.directory(None)

def test_directory_value_empty(validator):
    with pytest.raises(InvalidConfigValueError, match='cannot be empty'):
        validator.directory('')

def test_directory_value_bad_type(validator):
    with pytest.raises(InvalidConfigValueError, match='must be a string'):
        validator.directory(99)

def test_directory_value_not_absolute(validator):
    with pytest.raises(InvalidConfigValueError, match='must be an absolute path'):
        validator.directory('test')

def test_directory_value_not_exists(validator):
    with pytest.raises(InvalidConfigValueError, match='does not exist'):
        validator.directory('/test')

def test_directory_value_not_dir(validator):
    with pytest.raises(InvalidConfigValueError, match='is not a directory'):
        validator.directory(__file__)

@pytest.mark.parametrize('check_absolute_path, check_exists, check_is_dir', [
    (True, True, True),
    (True, True, False),
    (True, False, True),
    (True, False, False),
    (False, True, True),
    (False, True, False),
    (False, False, True),
    (False, False, False)
    ])
def test_directory_flags_valid(validator, project_root, check_absolute_path, check_exists, check_is_dir):
    assert validator.directory(
        project_root,
        check_absolute_path=check_absolute_path,
        check_exists=check_exists,
        check_is_dir=check_is_dir
    ) is True


# testing filename method
def test_filename_value_valid(validator):
    assert validator.filename('validator_test.py') is True

def test_filename_value_none(validator):
    with pytest.raises(InvalidConfigValueError, match='cannot be None'):
        validator.filename(None)

def test_filename_value_empty(validator):
    with pytest.raises(InvalidConfigValueError, match='cannot be empty'):
        validator.filename('')

def test_filename_value_bad_type(validator):
    with pytest.raises(InvalidConfigValueError, match='must be a string'):
        validator.filename(99)

def test_filename_value_invalid_chars(validator):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        with pytest.raises(InvalidConfigValueError, match='contains one or more invalid characters'):
            validator.filename(f"test{char}.py")

def test_filename_contains_unsafe_path_sequence(validator):
    with pytest.raises(InvalidConfigValueError, match='contains a potentially unsafe path sequence'):
        validator.filename('test..test.py')

def test_filename_contains_unsafe_path_sequence_check_disabled(validator):
    # This should not raise an exception because check_path_seq is False
    assert validator.filename('test..test.py', check_path_seq=False) is True

def test_filename_custom_invalid_chars(validator):
    with pytest.raises(InvalidConfigValueError, match='contains one or more invalid characters'):
        validator.filename('test#.py', invalid_chars=['#'])


# testing url method
def test_url_value_valid(validator):
    assert validator.url('https://www.google.com') is True

def test_url_value_none(validator):
    with pytest.raises(InvalidConfigValueError, match='cannot be None'):
        validator.url(None)

def test_url_value_empty(validator):
    with pytest.raises(InvalidConfigValueError, match='cannot be empty'):
        validator.url('')

def test_url_value_bad_type(validator):
    with pytest.raises(InvalidConfigValueError, match='must be a string'):
        validator.url(99)

def test_url_value_no_scheme(validator):
    with pytest.raises(InvalidConfigValueError, match='must have a valid scheme'):
        validator.url('www.google.com')

def test_url_value_no_domain(validator):
    with pytest.raises(InvalidConfigValueError, match='must have a valid domain'):
        validator.url('https://')

def test_url_value_invalid_scheme(validator):
    with pytest.raises(InvalidConfigValueError, match='must have a valid scheme'):
        validator.url('ftp://www.google.com')

def test_url_flags_scheme_false_invalid_scheme(validator):
    assert validator.url(
        'ftp://www.google.com',
        check_scheme=False,
        check_domain=True
    ) is True

def test_url_flags_domain_false_no_domain(validator):
    assert validator.url(
        'https://',
        check_scheme=True,
        check_domain=False
    ) is True

@pytest.mark.parametrize('check_scheme, check_domain', [
    (True, True),
    (True, False),
    (False, True),
    (False, False)
    ])
def test_url_flags_valid(validator, check_scheme, check_domain):
    assert validator.url(
        'https://www.google.com',
        check_scheme=check_scheme,
        check_domain=check_domain
    ) is True


# testing api_token method
def test_token_value_valid(validator):
    assert validator.api_token('test') is True

def test_token_value_none(validator):
    with pytest.raises(InvalidConfigValueError, match='cannot be None'):
        validator.api_token(None)

def test_token_value_empty(validator):
    with pytest.raises(InvalidConfigValueError, match='cannot be empty'):
        validator.api_token('')

def test_token_value_bad_type(validator):
    with pytest.raises(InvalidConfigValueError, match='must be a string'):
        validator.api_token(99)

def test_token_expected_length(validator):
    with pytest.raises(InvalidConfigValueError, match='must be 5 characters'):
        validator.api_token('test', expected_length=5)

def test_token_expected_prefix(validator):
    with pytest.raises(InvalidConfigValueError, match='must start with abc'):
        validator.api_token('test', expected_prefix='abc')

def test_token_expected_suffix(validator):
    with pytest.raises(InvalidConfigValueError, match='must end with xyz'):
        validator.api_token('test', expected_suffix='xyz')

def test_token_invalid_chars(validator):
    with pytest.raises(InvalidConfigValueError, match='contains one or more invalid characters'):
        validator.api_token('test@123', invalid_chars=['@', '#'])
