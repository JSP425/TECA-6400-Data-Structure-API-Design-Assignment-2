import random
import string
import project2pipeline as pro

import pytest

@pytest.fixture
def random_number():
    num=random.random()
    # print(f"randomnum={num}")

    return num



@pytest.fixture
def DataManagerInstance(tmpdir):
    return pro.DataManager(tmpdir.strpath)

@pytest.fixture
def DirectoryOfShowsInstance(tmpdir):
    return pro.DirectoryOfShows(tmpdir.strpath, "Assignee1", "Creator1")

@pytest.fixture
def ShowInstance(tmpdir):
    return pro.Show(tmpdir.strpath, "Producer1", "Director1", "Creator2")

@pytest.fixture
def ShotInstance(tmpdir):
    return pro.Shot(tmpdir.strpath, 1, 23.97, 1, 24, "Creator3")

@pytest.fixture
def AssetInstance(tmpdir):
    return pro.Asset(tmpdir.strpath, "character")

@pytest.fixture
def allInstances(tmpdir):
    return pro.DataManager(tmpdir.strpath), pro.DirectoryOfShows(tmpdir.strpath, "Assignee1", "Creator1"), pro.Shot(tmpdir.strpath, 1, 23.97, 1, 24, "Creator3"), pro.Asset(tmpdir.strpath, "character")



@pytest.fixture
def updatedata(tmpdir):
    pass
    