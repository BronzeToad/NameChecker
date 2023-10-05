import pytest

from cfg.config_helper import ConfigHelper
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


def test_batch_size(mock_config_parser, env_type):
    cfg = ConfigHelper(env_type)
    assert cfg.batch_size == 25

def test_batch_retries(mock_config_parser, env_type):
    cfg = ConfigHelper(env_type)
    assert cfg.batch_retries == 3