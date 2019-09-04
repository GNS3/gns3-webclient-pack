# -*- coding: utf-8 -*-
import pytest
import os
import tempfile
import sys
sys._called_from_test = True

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# We can get a segfault if the QT application is not initialized
#from gns3_webclient_pack.qt.QtWidgets import QApplication
#app = QApplication([])

@pytest.fixture
def local_config():

    from gns3_webclient_pack.local_config import LocalConfig
    (fd, config_path) = tempfile.mkstemp()
    os.close(fd)
    LocalConfig._instance = LocalConfig(config_file=config_path)
    return LocalConfig.instance()
