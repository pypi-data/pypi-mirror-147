# import pytest

from . import services


# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_itemcollected(item):
    services.logger.dbg(f"JAX: item:{item}")
