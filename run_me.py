import project2pipeline as pipe


# input your own root directory below and run
targetDirectory = "C:/Users/jpark/Desktop/TestDirectory" 

# these do not need to be modified
show1 = targetDirectory+"/Show1"
show2 = targetDirectory+"/Show2"

shot1 = show1 + "/Shot1"
shot2 = show1 + "/Shot2"
shot3 = show2 + "/Shot3"
shot4 = show2 + "/Shot4"

asset1 = show1 + "/Asset1"
asset2 = show1 + "/Asset2"
asset3 = show2 + "/Asset3"
asset4 = show2 + "/Asset4"

# ====================================== Creating the directories ======================================

maindir=pipe.DirectoryOfShows(targetDirectory, "Assigned1", "Creator1")

show1=pipe.Show(show1, "Producer1", "Director1", "Creator1")
show2=pipe.Show(show2, "Producer2", "Director2", "Creator2")

shot1=pipe.Shot(shot1, 1, 23.97, 1, 140, "Creator1")
shot2=pipe.Shot(shot2, 2, 23.97, 141, 251, "Creator1")
shot3=pipe.Shot(shot3, 3, 23.97, 252, 278, "Creator2")
shot4=pipe.Shot(shot4, 4, 23.97, 279, 300, "Creator2")

asset1=pipe.Asset(asset1, "character")
asset2=pipe.Asset(asset2, "character")
asset3=pipe.Asset(asset3, "prop")
asset4=pipe.Asset(asset4, "environment")

# ====================================== Making Associations ======================================

asset1.associateAssetShot("Asset1",1)
asset1.associateAssetShot("Asset1", 2)
asset2.associateAssetShot("Asset2",2)

asset3.associateAssetShot("Asset3",3)
asset3.associateAssetShot("Asset3",4)
asset4.associateAssetShot("Asset4",4)


# ====================================== Reading Info ======================================

show1.showAssetList()
show2.showAssetList()

asset1.showShotAssociationFor("Asset1")
shot3.showAssetAssociationFor(4)

# ====================================== Archiving ======================================

asset1.archiveZip("Asset1")
show2.archiveZipShow("Show2")

# ====================================== Reading Info after archive ======================================

asset1.showArchiveContent("Asset1.zip")
asset1.showArchivedDatabase("Asset1")


# below shows how a user would access an archived folder in a separate python session
# replace the path below with the path for the Asset 

# other=pipe.DataManager("C:/Users/jpark/Desktop/TestDirectory/Show1/Asset1")

# other.showArchiveContent("Asset1.zip")
# other.showArchivedDatabase("Asset1")

