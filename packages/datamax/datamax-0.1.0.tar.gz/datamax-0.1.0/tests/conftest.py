import os
from shutil import rmtree

import pytest


@pytest.fixture
def basic_filepath():
    return "examples/basic.cargofile"


@pytest.fixture
def cleanup():
    to_delete = []
    yield to_delete
    for item in to_delete:
        if os.path.exists(item):
            rmtree(item)
