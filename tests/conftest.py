# -*- coding: utf-8 -*-
import pytest
import os
import tempfile
import sys
sys._called_from_test = True

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def local_config():

    from gns3_webclient_pack.local_config import LocalConfig
    (fd, config_path) = tempfile.mkstemp()
    os.close(fd)
    LocalConfig._instance = LocalConfig(config_file=config_path)
    return LocalConfig.instance()


def pytest_configure(config):
    """
    Use to detect in code if we are running from pytest

    http://pytest.org/latest/example/simple.html#detect-if-running-from-within-a-pytest-run
    """
    import sys
    sys._called_from_test = True


def pytest_unconfigure(config):
    del sys._called_from_test
