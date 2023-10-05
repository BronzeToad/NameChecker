import pytest

from cfg.config_helper import ConfigHelper, EnvType
from tests.conftest import MOCK_CONFIG, MOCK_SECRETS


# =============================================================================================== #

@pytest.mark.parametrize(
    'section, key', [
        ('Directory', 'OUTPUT'),
        ('Filename', 'RESULTS'),
        ('GoDaddy', 'DEV_API_URL'),
        ('GitHub', 'BASE_API_URL')
    ])
def test_get_config_val(mock_config_parser, env_type, section, key):
    cfg = ConfigHelper(env_type)
    assert cfg.get_config_val(section, key) == MOCK_CONFIG[section][key]


@pytest.mark.parametrize(
    'section, key', [
        ('GoDaddy', 'DEV_API_KEY'),
        ('GoDaddy', 'DEV_API_SECRET'),
        ('GitHub', 'TOKEN')
    ])
def test_get_secret_val(mock_config_parser, env_type, section, key):
    cfg = ConfigHelper(env_type)
    assert cfg.get_config_val(section, key) == MOCK_SECRETS[section][key]


def test_clean_returned_val(mock_config_parser, env_type):
    pass    # TODO: Implement this test


def test_batch_size(mock_config_parser, env_type):
    cfg = ConfigHelper(env_type)
    assert cfg.batch_size == 25

def test_batch_retries(mock_config_parser, env_type):
    cfg = ConfigHelper(env_type)
    assert cfg.batch_retries == 3

def test_root_dir(mock_config_parser, env_type):
    cfg = ConfigHelper(env_type)
    assert cfg.root_dir == '/Users/Spock/Documents/Projects/NameChecker'

def test_config_dir(mock_config_parser, env_type):
    cfg = ConfigHelper(env_type)
    assert cfg.config_dir == '/Users/Spock/Documents/Projects/NameChecker/cfg'

def test_output_dir(mock_config_parser, env_type):
    cfg = ConfigHelper(env_type)
    assert cfg.output_dir == '/Users/Spock/Documents/Projects/NameChecker/output'

def test_seeds_filename(mock_config_parser, env_type):
    cfg = ConfigHelper(env_type)
    assert cfg.seeds_filename == 'seeds.json'

def test_results_filename(mock_config_parser, env_type):
    cfg = ConfigHelper(env_type)
    if env_type == EnvType.PRD:
        assert cfg.results_filename == 'results.json'
    else:
        assert cfg.results_filename == 'test_results.json'

def test_godaddy_max_retries(mock_config_parser, env_type):
    cfg = ConfigHelper(env_type)
    assert cfg.godaddy_max_retries == 3

def test_godaddy_api_url(mock_config_parser, env_type):
    cfg = ConfigHelper(env_type)
    if env_type == EnvType.PRD:
        assert cfg.godaddy_api_url == 'https://api.godaddy.com/v1/domains/available'
    else:
        assert cfg.godaddy_api_url == 'https://api.ote-godaddy.com/v1/domains/available'

def test_godaddy_api_key(mock_config_parser, env_type):
    cfg = ConfigHelper(env_type)
    if env_type == EnvType.PRD:
        assert cfg.godaddy_api_key == '7IkYeMLOxndchArW0Bb7niGBOG0YDn-tKi'
    else:
        assert cfg.godaddy_api_key == 'ZKeW4PngucIXUcGtcRio9eslmfqxJgN7Svez9'

def test_godaddy_api_secret(mock_config_parser, env_type):
    cfg = ConfigHelper(env_type)
    if env_type == EnvType.PRD:
        assert cfg.godaddy_api_secret == 'ExDSUaOJHZGBoifcO-HBeP'
    else:
        assert cfg.godaddy_api_secret == '02b4NyuxC_qT7HoIajmiD8'

def test_github_api_url(mock_config_parser, env_type):
    cfg = ConfigHelper(env_type)
    assert cfg.github_api_url == 'https://api.github.com/users/'

def test_github_token(mock_config_parser, env_type):
    cfg = ConfigHelper(env_type)
    assert cfg.github_token == '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'
