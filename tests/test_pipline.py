import project2pipeline
#from project2pipeline import DataManager, DirectoryOfShows, Show, Shot, Asset
import pytest
import json
import os


targetDirectory="C:/Users/jpark/Desktop/TestDirectory"
targetShow="C:/Users/jpark/Desktop/TestDirectory/Show1"
targetShot="C:/Users/jpark/Desktop/TestDirectory/Show1/Shot1"
targetShot2="C:/Users/jpark/Desktop/TestDirectory/Show1/Shot2"

targetAsset="C:/Users/jpark/Desktop/TestDirectory/Show1/Asset1"
targetAsset2="C:/Users/jpark/Desktop/TestDirectory/Show1/Asset2"

targetDB="C:/Users/jpark/Desktop/TestDirectory/Show1/Shot1/Shot1 Database"



def test_random(random_number):
    print(random_number)
    assert type(random_number) == float


def test_directoryOfShows(DirectoryOfShowsInstance: project2pipeline.DirectoryOfShows):
    assert isinstance(DirectoryOfShowsInstance, project2pipeline.DirectoryOfShows)

def test_show(ShowInstance: project2pipeline.Show):
    assert isinstance(ShowInstance, project2pipeline.Show)

def test_asset(AssetInstance: project2pipeline.Asset):
    assert isinstance(AssetInstance, project2pipeline.Asset)

def test_existDelete(DataManagerInstance: project2pipeline.DataManager):

    project2pipeline.DirectoryOfShows(targetDirectory, "Assignee", "Creator1000",)
    project2pipeline.Show(targetShow, "Producer99", "Director99", "Creator99")
    project2pipeline.Shot(targetShot, 1, 23.97, 1, 40, "ArtistName")
    project2pipeline.Asset(targetAsset, "character") 

    DataManagerInstance.removeFolder(targetAsset)
    DataManagerInstance.removeFolder(targetShot)
    DataManagerInstance.removeFolder(targetShow)
    DataManagerInstance.removeFolder(targetDirectory)


def test_updateDatabase():
    project2pipeline.DirectoryOfShows(targetDirectory, "Assignee", "Creator1000",)
    project2pipeline.Show(targetShow, "Producer99", "Director99", "Creator99")
    project2pipeline.Shot(targetShot, 1, 23.97, 1, 40, "ArtistName")
    temp=project2pipeline.Asset(targetAsset, "character") 

    temp.updateDatabase("Shot1 Database", "assigned animators", ["Artist 1", "Artist 2", "Artist 3"])
    with open(targetDB,'r') as file:
        data = json.load(file)
        data['assigned animators'] = ["Artist 1", "Artist 2", "Artist 3"]

    assert data['assigned animators'] == ["Artist 1", "Artist 2", "Artist 3"]

    temp.removeFolder(targetDirectory)

# def test_all(allInstances: project2pipeline):
#     allInstances.d

def test_associate():
    project2pipeline.DirectoryOfShows(targetDirectory, "Assignee", "Creator1000",)
    project2pipeline.Show(targetShow, "Producer99", "Director99", "Creator99")
    project2pipeline.Shot(targetShot, 1, 23.97, 1, 40, "ArtistName")
    project2pipeline.Shot(targetShot2, 2, 23.97, 1, 40, "ArtistName2")
    temp=project2pipeline.Asset(targetAsset, "character")
    project2pipeline.Asset(targetAsset2, "prop")

    temp.associateAssetShot("Asset1", 1)
    temp.associateAssetShot("Asset2", 1)
    temp.associateAssetShot("Asset2", 2)

    a2association=temp.showShotAssociationFor("Asset2")
    s1association=temp.showAssetAssociationFor(1)

    resultAsset = temp.showADBforAssetKey("Asset1")
    resultShot = temp.showADBforShotKey(1)

    charResult=temp.showCharacterCategory()
    propResult=temp.showPropCategory()

    assert a2association == [1,2]
    assert s1association == ["Asset1", "Asset2"]

    assert resultAsset == [1]
    assert resultShot == ["Asset1", "Asset2"]

    assert charResult == ["Asset1"]
    assert propResult == ["Asset2"]

    temp.removeFolder(targetDirectory)

def test_archiveZipAsset():
    project2pipeline.DirectoryOfShows(targetDirectory, "Assignee", "Creator1000",)
    show=project2pipeline.Show(targetShow, "Producer99", "Director99", "Creator99")
    project2pipeline.Shot(targetShot, 1, 23.97, 1, 40, "ArtistName")
    project2pipeline.Shot(targetShot2, 2, 23.97, 1, 40, "ArtistName2")
    temp=project2pipeline.Asset(targetAsset, "character")
    project2pipeline.Asset(targetAsset2, "prop")

    temp.archiveZip("Asset1")
    temp.archiveZip("Asset2")

    # result=temp.showDatabaseKey("Asset1 Database", "category")

    assert os.path.exists(targetAsset+".zip")
    assert os.path.exists(targetAsset2+".zip")
    
    assert os.path.exists(targetAsset) == False
    assert os.path.exists(targetAsset2) == False

    # assert result == "character"

    temp.removeFolder(targetDirectory)

def test_archiveZipShow():
    project2pipeline.DirectoryOfShows(targetDirectory, "Assignee", "Creator1000",)
    show=project2pipeline.Show(targetShow, "Producer99", "Director99", "Creator99")
    project2pipeline.Shot(targetShot, 1, 23.97, 1, 40, "ArtistName")
    project2pipeline.Shot(targetShot2, 2, 23.97, 1, 40, "ArtistName2")
    asset=project2pipeline.Asset(targetAsset, "character")
    project2pipeline.Asset(targetAsset2, "prop")

    asset.archiveZip("Asset1")
    result = asset.showArchiveContent("Asset1.zip")

    assert result == ['Asset1/', 'Asset1/Asset1 Database']

    # show.archiveZip("Show1")

    # categoryResult=asset.showCharacterCategory()

    # assert categoryResult == ["Asset1"]

