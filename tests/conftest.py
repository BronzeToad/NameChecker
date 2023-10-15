import pytest
from src.utils.config_helper import ConfigHelper, EnvType

# =============================================================================================== #

# Fixture to provide EnvType values
@pytest.fixture(params=list(EnvType))
def env_type(request):
    return request.param

@pytest.fixture
def config_helper(env_type):
    return ConfigHelper(env_type, test_mode=True)
