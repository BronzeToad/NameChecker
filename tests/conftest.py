import pytest
from src.utils.config_helper import EnvType

# =============================================================================================== #

# Fixture to provide EnvType values
@pytest.fixture(params=list(EnvType))
def env_type(request):
    return request.param
