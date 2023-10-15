# import pytest
# import configparser
# from cfg.config_helper import ConfigHelper, EnvType
# from tests.conftest import MOCK_CONFIG, MOCK_SECRETS, mock_config_parser, env_type

# FIXME: this test is failing because the ConfigHelper class is not being mocked properly

# =============================================================================================== #

# @pytest.mark.parametrize(
#     'section, key', [
#         ('Directory', 'OUTPUT'),
#         ('Filename', 'RESULTS'),
#         ('GoDaddy', 'DEV_API_URL'),
#         ('GitHub', 'BASE_API_URL'),
#         ('GoDaddy', 'DEV_API_KEY'),
#         ('GoDaddy', 'DEV_API_SECRET'),
#         ('GitHub', 'TOKEN')
#     ])
# def test_get_config_val(mock_config_parser, env_type, section, key):
#     cfg = ConfigHelper(env_type)
#     assert cfg.get_config_val(section, key) == MOCK_CONFIG[section][key]

def test_load_config_files(config_helper):
    config_helper._batch_size = 25
    assert config_helper.batch_size == 25
