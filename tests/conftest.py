import os
import shutil
import time

import pytest

@pytest.fixture(scope="session", autouse=True)
def sandbox():
    print("Creating sandbox")
    sbox = os.path.join(os.path.dirname(__file__), 'sandbox')
    if os.path.exists(sbox):
        shutil.rmtree(sbox)
    os.mkdir(sbox)
    cwd = os.getcwd()
    os.chdir(sbox)
    yield
    os.chdir(cwd)
    time.sleep(0.5)  # prevents errors when removing sandbox dir
    shutil.rmtree(sbox)
