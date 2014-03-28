import os
import shutil
import time


def setup():
    sbox = os.path.join(os.path.dirname(__file__), 'sandbox')
    if os.path.exists(sbox):
        teardown()
    os.mkdir(sbox)
    os.chdir(sbox)


def teardown():
    os.chdir(os.path.dirname(__file__))
    time.sleep(0.5)  # prevents errors when removing sandbox dir
    shutil.rmtree(os.path.join(os.path.dirname(__file__), 'sandbox'))
