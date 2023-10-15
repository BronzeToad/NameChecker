import pytest

from src.utils.config_helper import EnvType


# =============================================================================================== #

# testing config loads
def test_load_batch_config(config_helper):
    assert 'Batch' in config_helper.config.sections()

def test_load_filename_config(config_helper):
    assert 'Filename' in config_helper.config.sections()

def test_load_godaddy_config(config_helper):
    assert 'GoDaddy' in config_helper.config.sections()

def test_load_github_config(config_helper):
    assert 'GitHub' in config_helper.config.sections()


# testing batch_size property
def test_batch_size_default(config_helper):
    assert config_helper.batch_size == 25

def test_batch_size_setter(config_helper):
    new_val = 50
    config_helper.batch_size = new_val
    assert config_helper.batch_size == new_val

def test_batch_size_invalid(config_helper):
    with pytest.raises(ValueError):
        config_helper.batch_size = 0


# testing batch_retries property
def test_batch_retries_default(config_helper):
    assert config_helper.batch_retries == 3

def test_batch_retries_setter(config_helper):
    new_val = 5
    config_helper.batch_retries = new_val
    assert config_helper.batch_retries == new_val

def test_batch_retries_invalid(config_helper):
    with pytest.raises(ValueError):
        config_helper.batch_retries = -1


# testing seeds_filename property
def test_seeds_filename_default(config_helper):
    assert config_helper.seeds_filename == 'seeds.json'

def test_seeds_filename_setter(config_helper):
    new_filename = 'bad_seeds.pdf'
    config_helper.seeds_filename = new_filename
    assert config_helper.seeds_filename == new_filename

def test_seeds_filename_invalid(config_helper):
    with pytest.raises(ValueError):
        config_helper.seeds_filename = ''


# testing results_filename property
def test_results_filename_default(config_helper):
    if config_helper.env_type == EnvType.PRD:
        assert config_helper.results_filename == 'results.json'
    else:
        assert config_helper.results_filename == 'test_results.json'

def test_results_filename_setter(config_helper):
    new_filename = 'bad_results.pdf'
    config_helper.results_filename = new_filename
    assert config_helper.results_filename == new_filename

def test_results_filename_invalid(config_helper):
    with pytest.raises(ValueError):
        config_helper.results_filename = ''


# testing godaddy_max_retries property
def test_godaddy_max_retries_default(config_helper):
    assert config_helper.godaddy_max_retries == 3

def test_godaddy_max_retries_setter(config_helper):
    new_val = 5
    config_helper.godaddy_max_retries = new_val
    assert config_helper.godaddy_max_retries == new_val

def test_godaddy_max_retries_invalid(config_helper):
    with pytest.raises(ValueError):
        config_helper.godaddy_max_retries = -1


# testing godaddy_api_url property
def test_godaddy_api_url_default(config_helper):
    if config_helper.env_type == EnvType.PRD:
        assert config_helper.godaddy_api_url == 'https://api.godaddy.com'
    else:
        assert config_helper.godaddy_api_url == 'https://api.ote-godaddy.com'

def test_godaddy_api_url_setter(config_helper):
    new_url = 'https://youtu.be/dQw4w9WgXcQ'
    config_helper.godaddy_api_url = new_url
    assert config_helper.godaddy_api_url == new_url

def test_godaddy_api_url_invalid(config_helper):
    with pytest.raises(ValueError):
        config_helper.godaddy_api_url = ''


# testing github_api_url property
def test_github_api_url_default(config_helper):
    assert config_helper.github_api_url == 'https://api.github.com'

def test_github_api_url_setter(config_helper):
    new_url = 'https://youtu.be/dQw4w9WgXcQ'
    config_helper.github_api_url = new_url
    assert config_helper.github_api_url == new_url

def test_github_api_url_invalid(config_helper):
    with pytest.raises(ValueError):
        config_helper.github_api_url = ''


# testing godaddy_api_key property
def test_godaddy_api_key_default(config_helper):
    if config_helper.env_type == EnvType.PRD:
        assert config_helper.godaddy_api_key == 'TEST_prd_api_key_456'
    else:
        assert config_helper.godaddy_api_key == 'TEST_dev_api_key_123'

def test_godaddy_api_key_setter(config_helper):
    new_key = 'nEvErGoNnAGiVeYoUuP'
    config_helper.godaddy_api_key = new_key
    assert config_helper.godaddy_api_key == new_key

def test_godaddy_api_key_invalid(config_helper):
    with pytest.raises(ValueError):
        config_helper.godaddy_api_key = ''


# testing godaddy_api_secret property
def test_godaddy_api_secret_default(config_helper):
    if config_helper.env_type == EnvType.PRD:
        assert config_helper.godaddy_api_secret == 'TEST_prd_api_secret_456'
    else:
        assert config_helper.godaddy_api_secret == 'TEST_dev_api_secret_123'

def test_godaddy_api_secret_setter(config_helper):
    new_secret = 'nEvErGoNnALeTyoUdOwN'
    config_helper.godaddy_api_secret = new_secret
    assert config_helper.godaddy_api_secret == new_secret

def test_godaddy_api_secret_invalid(config_helper):
    with pytest.raises(ValueError):
        config_helper.godaddy_api_secret = ''


# testing github_token property
def test_github_token_default(config_helper):
    assert config_helper.github_token == 'github_pat_TEST_token_123'

def test_github_token_setter(config_helper):
    new_token = 'github_pat_nEvErGoNnArUnArOuNdAnDdEsErTyOu'
    config_helper.github_token = new_token
    assert config_helper.github_token == new_token

def test_github_token_invalid(config_helper):
    with pytest.raises(ValueError):
        config_helper.github_token = ''


@pytest.mark.parametrize(
    'section, key', [
        ('Batch', 'BATCH_SIZE'),
        ('Filename', 'SEEDS'),
        ('GoDaddy', 'DEV_API_URL'),
        ('GoDaddy', 'DEV_API_KEY'),
        ('GitHub', 'BASE_API_URL'),
        ('GitHub', 'TOKEN')
    ])
def test_get_config_val(config_helper, section, key):
    assert config_helper.get_config_val(section, key) == config_helper.config[section][key]
