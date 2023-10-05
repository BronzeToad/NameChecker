import pytest
from unittest.mock import patch
from cfg.config_helper import EnvType


# =============================================================================================== #

MOCK_CONFIG = {
    'Batch': {
        'BATCH_SIZE': '25',
        'BATCH_RETRIES': '3'
    },
    'Directory': {
        'ROOT': '/Users/Spock/Documents/Projects/NameChecker',
        'CONFIG': '/Users/Spock/Documents/Projects/NameChecker/cfg',
        'OUTPUT': '/Users/Spock/Documents/Projects/NameChecker/output'
    },
    'Filename': {
        'SEEDS': 'seeds.json',
        'RESULTS': 'results.json',
        'TST_RESULTS': 'test_results.json'
    },
    'GoDaddy': {
        'DEV_API_URL': 'https://api.ote-godaddy.com/v1/domains/available',
        'PRD_API_URL': 'https://api.godaddy.com/v1/domains/available',
        'MAX_RETRIES': '3'
    },
    'GitHub': {
        'BASE_API_URL': 'https://api.github.com/users/'
    }
}

MOCK_SECRETS = {    # These are not real secrets, just random strings
    'GoDaddy': {
        'DEV_API_KEY'   : 'ZKeW4PngucIXUcGtcRio9eslmfqxJgN7Svez9',
        'DEV_API_SECRET': '02b4NyuxC_qT7HoIajmiD8',
        'PRD_API_KEY'   : '7IkYeMLOxndchArW0Bb7niGBOG0YDn-tKi',
        'PRD_API_SECRET': 'ExDSUaOJHZGBoifcO-HBeP'
    },
    'GitHub': {
        'TOKEN': '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'
    }
}


# =============================================================================================== #

@pytest.fixture(scope="function")
def mock_config_parser():
    """Fixture to mock the configparser.ConfigParser for reading configurations."""
    with patch("configparser.ConfigParser.read"), \
         patch("configparser.ConfigParser.__getitem__") as mock_getitem, \
         patch("configparser.ConfigParser.get") as mock_get:
        # Ensure that the get method returns the correct values
        def side_effect_get(section, key):
            return MOCK_CONFIG.get(section, {}).get(key) or MOCK_SECRETS.get(section, {}).get(key)


        mock_get.side_effect = side_effect_get
        mock_getitem.side_effect = lambda section: MOCK_CONFIG.get(section, {})

        yield


@pytest.fixture(params=list(EnvType))
def env_type(request):
    """Fixture to parameterize tests based on EnvType values."""
    return request.param


# =============================================================================================== #

"""
def test_some_function_using_config_helper(mock_config_parser, env_type):
    config_helper = ConfigHelper(env_type=env_type)
    # ... Your test logic for the function ...

def test_another_function_using_config_helper(mock_config_parser, env_type):
    config_helper = ConfigHelper(env_type=env_type)
    # ... Your test logic for another function ...
"""
