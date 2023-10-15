import pytest

import src.utils.toad_utils as ToadUtils
from src.utils.config_helper import ConfigHelper, EnvType
from src.utils.validator import ValidatorType, Validator

# =============================================================================================== #

# Fixture to provide EnvType values
@pytest.fixture(params=list(EnvType))
def env_type(request):
    return request.param

@pytest.fixture
def config_helper(env_type):
    return ConfigHelper(env_type, test_mode=True)

@pytest.fixture
def toad_utils():
    return ToadUtils

@pytest.fixture
def project_root(toad_utils):
    return toad_utils.find_project_root('NameChecker', test_mode=True)

@pytest.fixture
def validator():
    return Validator(ValidatorType.CONFIG)
