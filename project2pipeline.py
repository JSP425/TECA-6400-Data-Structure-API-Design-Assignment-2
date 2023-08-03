import os
import json
import shutil
import zipfile
from typing import Any, Union


"will need to load a target directory vs the highlest when creating data manager class as associations DB will all have same name within each show"
class DataManager:
    """Creates a general data manager instance. 
    
    This class should be used to manage an existing directory. There are three major types of methods: Path Manipulating Methods,
    Database Methods and Data Retrieval Methods. Its initialization takes in a file path and the user should input an exist directory to begin
    managing it. A non-existing directory can be input where a new general directory will be created without automatically populated databases.
    
    typical usage:

    instance = DataManager(C:/Users/jpark/Desktop/TestDirectory/Show1/Asset1")
    """
    def __init__(self, filePath: str, creator="default creator name") -> None:
         
        self.name = self.getLastPathItem(filePath)
        self.creator = creator
        self.filePath = filePath
        #self.databasename = "default database"
        self.databasePath = None 

        self.shotAssociationsDB = "Shot-Asset Associations Database"
        self.assetAssociationsDB = "Asset-Shot Associations Database"
        self.categoryAssociationsDB = "Assets by Categories Database"

        self.categoryCharacterKey = "character"
        self.categoryPropKey = "prop"
        self.categoryEnvironmentKey = "environment"

        path=os.path.join(self.filePath) # if only 1 argument, useful for turning \ into /

        if os.path.exists(path) == True:
            print(f"Current Directory Set To: {self.filePath}")
        else:
            print("============================== Updated Directory ============================== ")
            print(f"Added directory: {path}")
            os.makedirs(path)

            self.createDatabase()
            self.writeDatabase(self.name + " Database")

    # ======================================================== Path Manipulating Methods ================================================

    def makePath(self,*pathargs: str) -> str:
       """
       Create new path with argument value.

       This method will take the initialized path and join it with the argument provided. 
       It is mostly used by other functions in this module
       """

       path=os.path.join(self.filePath, "/".join(pathargs))
       # if pathargs contains self.filePath in it, it will still work. seems like os.path.join will be smart and not duplicate a part of the path
       # print(f"makepath: {path}")
       return path

    def getFilePath(self, file_name: str, directory_path: str) -> str:
        """
        Get a file path based on file name.

        First argument is the file name to be searched for and the second argument specifies from which directory to begin searching.
        If the file exists, it will retun the path to that file.
        The second argument is typically self.filePath and is mostly used by other functions in this module.
        """
        for root, dirs, files in os.walk(directory_path):
            if file_name in files:
                file_path = os.path.join(root, file_name)
                print("File found at:", file_path)
                return file_path

        # File not found
        else:
            print("File not found.")
            return None
    
    def getFilePathFromParent(self, file_name: str, directory_path: str) -> str:
        """
        Get a file path based on file name.

        First argument is the file name to be searched for and the second argument specifies from which PARENT directory to begin searching.
        This is slightly different from the getFilePath method as it starts it file search from the parent of the specified directory -usually
        self.filePath. This is mostly used by other methods and is useful for identifying json databases above the current directory.

        If the file exists, it will retun the path to that file.
        """

        parent_directory = os.path.dirname(directory_path)

        for root, dirs, files in os.walk(parent_directory):
            if file_name in files:
                file_path = os.path.join(root, file_name)
                print("File found at:", file_path)
                return file_path

        # File not found
        else:
            print(f"File {file_name} not found when starting to look from {parent_directory}.")
            return None
        
    def getDirectoryPathFromParent(self, targetDirectory: str, directory_path: str) -> str:
        """
        Get a directory path based on the end/target directory.

        First argument is the directory name to be searched for and the second argument specifies from which PARENT directory to begin searching.
        This is mostly used by zip/archiving methods.
        """
        parent_directory = os.path.dirname(directory_path)

        for root, dirs, files in os.walk(parent_directory):
            if targetDirectory in dirs:
                targetPath = os.path.join(root, targetDirectory)
                print("Directory found at:", targetPath)
                return targetPath

        # Directory not found
        else:
            print("Directory not found.")
            return None

    def getLastPathItem(self, targetPath: str) -> str:
        """
        Get a the final directory from a path as a string.
        """
        result = os.path.basename(targetPath)
        return result
        
    def getDirectoryPath(self, directory_name: str, directory_path: str) -> str:
        """
        Get a directory path based on directory name.

        First argument is the directory name to be searched for and the second argument specifies from which directory to begin searching.
        If the directory exists, it will retun the path to that directory.
        The second argument is typically self.filePath and is mostly used by other functions in this module.
        """
        for root, dirs, files in os.walk(directory_path):
            if directory_name in dirs:
                target_path = os.path.join(root, directory_name)
                print("File found at:", target_path)
                return target_path

        # File not found
        else:
            print(f"Directory {directory_name} not found inside {directory_path}.")
            return None

    def checkExist(self, folderName: str) -> Union[bool,str]:
        """
        Check if a folder exists.

        Given a folder name, it will check from parent directory of the current instance and downwards to see if that folder exists.
        If it does it will return the path to that folder. If not, it will return false.
        
        """

        parent_directory = os.path.dirname(self.filePath)

        targetExist = self.getDirectoryPath(folderName, parent_directory)

        if targetExist == None:
            return False
        else:
            result=os.path.exists(targetExist)
            return result    

        
    # ======================================================== Database Methods ================================================
    def createDatabase(self) -> None:
        """"Creates a dictionary with default fields."""
        print(f"============================== Database Created For {self.name} ==============================")
        self.database = {
            "name" : self.name ,
            "creator" : self.creator,
            "filePath" : self.filePath,
            "assigned" : "N/A",
            "producer" : "N/A",
            "director" : "N/A"
        }
    
    
    def writeDatabase(self, *args: str) -> None:
        """ Writes a dictionary into a json file. """
        print("============================== Created JSON File ==============================")
        self.databasePath=self.makePath(*args)
        with open(self.databasePath,'w') as file:
            json.dump(self.database, file, indent=4)
        print(f"added a file at {self.databasePath}")

    
    def updateDatabase(self, targetDB: str, key: str, value: Any) -> None:
        """
        Replaces the current value of a specified key.

        It reads in the current value from the json file, REPLACES the old value with the new and re-writes the entire dictionary back into the 
        json file. Updating associations database should be done with the updateAssociationsDatabase method.
        """

        with open(self.getFilePathFromParent(targetDB, self.filePath), "r") as file:
            tempDatabase = json.load(file)

        tempDatabase[key]=value

        print(f"**** Updated Database: {key} : {value} ****")

        with open(self.getFilePathFromParent(targetDB, self.filePath),'w') as file:
            json.dump(tempDatabase, file, indent=4)

    def updateAssociationsDatabase(self, targetDB: str, key: str, value: Any) -> None:
        """
        Replaces the current value of a specified key for specific databases.
        
        It reads in the current value from the json file, REPLACES the old value with the new and re-writes the entire dictionary back into the 
        json file. This is different from the updateDatabase method as this begins its search from the parent directory; this is intended as the 
        "Shot-Asset Associations Database", "Asset-Shot Associations Database" and "Assets by Categories Database" reside at the Show directory 
        level and would not be accesible if searched for from a Shot or Asset instance.
        """

        associationsDB = self.getFilePathFromParent(targetDB, self.filePath)

        with open(associationsDB, "r") as file:
            tempDatabase = json.load(file)

        tempDatabase[key]=value

        print(f"**** Updated Database: {key} : {value} ****")

        with open(associationsDB,'w') as file:
            json.dump(tempDatabase, file, indent=4)
     

    def addInDatabase(self, targetDB: str, key: str, value: Any) -> None:
        """
        Append values into a database

        This function reads in a dictionary from a json file and appends to a list for a specified key.
        
        """

        associationsDB = self.getFilePathFromParent(targetDB, self.filePath)

        with open(associationsDB, "r") as file:
            tempDatabase = json.load(file)
        
        tempDatabase[key].append(value)

        print(f"**** Updated Database: {key} : {value} ****")

        with open(associationsDB,'w') as file:
            json.dump(tempDatabase, file, indent=4)
    
        
    def associateAssetShot(self, assetName: str, shotNumber: int) -> None:
        """
        Add a shot and asset to each other's databases

        This function first checks to see if the specified asset and shot exists. If it does, it will add a shot to an asset's database and 
        and an asset to the shot's database. It also updates the overarching associations database at the Show level.


        """


        assetNamePath=self.checkExist(assetName)
        #print(f"************************asset name path {assetNamePath}")

        shotNumberPath=self.checkExist(f"Shot{shotNumber}")
        #print(f"************************shotNumber {shotNumber}")

        if assetNamePath and shotNumberPath:
            self.addInDatabase(assetName + " Database", "shot association", shotNumber)
            self.addInDatabase("Shot" + str(shotNumber) + " Database", "asset association", assetName)

            # the same association above is recorded in the databases below so that only these databases need to be retrieved for information
            # regarding assoications; this is preferred as an alternative function would need to loop through multiple directories.
            self.addInDatabase(self.assetAssociationsDB, assetName, shotNumber)
            self.addInDatabase(self.shotAssociationsDB, f"Shot{shotNumber}", assetName)

        else:
            if not assetNamePath:
                print(f"The asset '{assetName}' does not exist. Association not made. Please double-check.")
            if not shotNumberPath:
                print(f"The shot 'Shot{shotNumber}' does not exist. Association not made. Please double-check.")
    
    # ======================================================== Data Retrieval Methods ================================================

    def showDatabase(self, targetDB: str) -> None:
        """ Prints the dictionary in a json file """   
        with open(self.getFilePathFromParent(targetDB, self.filePath),'r') as file:
            print(file.read())

    def showDatabaseKey(self, targetDB: str, key: str) -> dict:
        """ Prints and returns the value of a key from a specified database """
        with open(self.getFilePathFromParent(targetDB, self.filePath),'r') as file:
            jsonData=json.load(file)

            value = jsonData.get(key, "Key not found")
            print(value)

            return value

    def showShotAssociationFor(self, assetName: str) -> dict:
        """ Prints and returns the associated shots for the specified asset """
        with open(self.getFilePathFromParent(assetName + " Database", self.filePath),'r') as file:
            jsonData=json.load(file)

            value = jsonData.get("shot association", "Key not found")
            print(value)
            return value
        
    def showAssetAssociationFor(self, shotNumber: int) -> dict:
        """ Prints and returns the associated assets for the specified shot """
        with open(self.getFilePathFromParent("Shot" + str(shotNumber) + " Database", self.filePath),'r') as file:
            jsonData=json.load(file)

            value = jsonData.get("asset association", "Key not found")
            print(value)
            return value
        
    def showADBforAssetKey(self, key: str) -> dict:
        """ Prints and returns all the shots associated to the specified asset """

        with open(self.getFilePathFromParent(self.assetAssociationsDB, self.filePath),'r') as file:
            jsonData=json.load(file)

            value = jsonData.get(key, "Key not found")
            print(value)
            return value
        
    def showADBforShotKey(self, key: str) -> dict:
        """ Prints and returns all the assets associated to the specified shot """
        with open(self.getFilePathFromParent(self.shotAssociationsDB, self.filePath),'r') as file:
            jsonData=json.load(file)

            value = jsonData.get("Shot"+str(key), "Key not found")
            print(value)
            return value
        
    def showCategoryAll(self) -> None:
        """ Prints the entire Assets by Categories Database """
        self.showDatabase(self.categoryAssociationsDB)

    def showCharacterCategory(self) -> None:
        """ Prints and returns all assets under the character category """
        value = self.showDatabaseKey(self.categoryAssociationsDB, "character")
        return value
    
    def showPropCategory(self) -> None:
        """ Prints and returns all assets under the prop category """
        value = self.showDatabaseKey(self.categoryAssociationsDB, "prop")
        return value
    
    def showEnvironmentCategory(self) -> None:
        """ Prints and returns all assets under the environment category """
        value = self.showDatabaseKey(self.categoryAssociationsDB, "environment")
        return value
        
    def showArchiveContent(self, folderName: str) -> list:
        """ Print and return the contents of a zipfile. """
        # get filepathfromparent b/c folder name will be a zip FILE
        targetPath=self.getFilePathFromParent(folderName, self.filePath)
        with zipfile.ZipFile(targetPath, "r") as zipTarget:
            zipContent=zipTarget.namelist()

            for eachItem in zipContent:
                print(eachItem)
            return zipContent
        
    def showArchivedDatabase(self, targetName: str) -> None:
        """ Print the dictionary in a json file that is within a zip file.  """
        zipFileName=targetName+".zip"
        zipFilePath=self.getFilePathFromParent(zipFileName, self.filePath)

        with zipfile.ZipFile(zipFilePath) as z:
            for filename in z.namelist():
                if filename == targetName+"/"+targetName+" Database":
                    # read the file
                    with z.open(filename) as f:
                        #return f.read().decode('utf-8')  # Return the contents as a string
                        # print(f.read())
                        print(f.read().decode('utf-8'))

        return None  # File not found in the ZIP archive


    # ======================================================== File/Directory Methods ================================================    

    def addContent(self, *args: str) -> None:
        """ Creates a new directory from the given file path. """
        print(f"============================== Added: {self.name} ============================== ")
        newpath=self.makePath(*args)

        if os.path.exists(newpath) == True:
            print("This file path already exists")
        else:
            print(f"Added show: {newpath}")
            os.makedirs(newpath)

    def getContent(self, *args: str) -> None:
        """ Prints contents of a directory """
        print(f"============================== Content: {self.name} ==============================")
        newpath=self.makePath(*args)

        contents=os.listdir(newpath)
        print(f"Contents of {newpath}: \n {contents}")
    
    def moveFile(self, sourcePath: str, destinationPath: str) -> None:
        """ Moves a file from one directory to another. """
        if os.path.exists(destinationPath):
            shutil.move(sourcePath,destinationPath)
        else:
            print("Invalid destination directory")
        
    def removeFile(self,*args: str) -> None:
        """ Deletes a file after checking that it exists. """
        print(f"============================== Updated: {self.name} ============================== ")
        newpath=self.makePath(*args)
        if os.path.exists(newpath):
            os.remove(newpath)
            print(f"{newpath} was removed")
        else:
            print("File does not exist.")
    
    def removeFolder(self, *args: str) -> None:
        """ Deletes a folder and all its contents. """
        print(f"============================== Updated: {self.name} ============================== ")
        newpath=self.makePath(*args)
        #path=os.path.join(self.filePath, "/".join(args))
        shutil.rmtree(newpath)    
        print(f"removed a directory and its contents at {newpath}")


    def archiveZip(self, folderName):
        """ Create a zip file containing the contents of a shot or asset. """
        targetPath=self.getDirectoryPathFromParent(folderName, self.filePath)
        parentPath = os.path.dirname(targetPath)
        shutil.make_archive(targetPath, 'zip', parentPath, folderName)
        #os.remove(targetPath)
        self.removeFolder(targetPath)

    def archiveZipShow(self, showName):
        """ Zip all assets and shot directories under a show directory. """
        targetPath=self.getDirectoryPathFromParent(showName, self.filePath)
        for each in os.listdir(targetPath):
            subDirPath=os.path.join(targetPath,each)
            if os.path.isdir(subDirPath) == True:
                shutil.make_archive(subDirPath,'zip',self.filePath, each)
                self.removeFolder(subDirPath)




class DirectoryOfShows(DataManager):
    """ Create the highest level directory which contains a series of show directories """
    def __init__(self, filePath: str, assigned: str, creator: str) -> None:
        self.assigned = assigned                                                 # <-- this needs to come before super()....or else line 152 will error; if super before, 
        super().__init__(filePath, creator)                                   # it will run createDatabase (go to parent class, and see a more specific one in child class) 
                                                                                    # before it gets to read self.assigned=assigned
    
    def createDatabase(self) -> None:
        """ Create a database specific for the DirectoryOfShows """
        print(f"============================== Database Created For {self.name} ==============================")
        self.database = {
            "name" : self.name ,
            "creator" : self.creator,
            "filePath" : self.filePath,
            "assigned" : self.assigned,     
        }


class Show(DataManager):
    """ Create a directory containing directories of assets and shots """
    def __init__(self, filePath: str, producer: str, director: str, creator: str) -> None:
        self.producer = producer
        self.director = director
        super().__init__(filePath, creator)



        print(f"============================== Added Show: {self.name} ============================== ")

        # these databases detail associations between shots and assets. it also lists categories that assets belong to
        # this information can be found in the databases under shots and assets but having mirroring databases at the show level make it
        # easer to retrieve this information later as opposed to looping through various directories and individual databases.
        # Create an empty database and write it under different names
        self.createAssociationsDatabase()
        self.writeDatabase(self.shotAssociationsDB)
        self.writeDatabase(self.assetAssociationsDB)
        self.writeDatabase(self.categoryAssociationsDB)

        # adding an empty list to each database
        self.updateAssociationsDatabase(self.categoryAssociationsDB, self.categoryCharacterKey, [])
        self.updateAssociationsDatabase(self.categoryAssociationsDB, self.categoryPropKey, [])
        self.updateAssociationsDatabase(self.categoryAssociationsDB, self.categoryEnvironmentKey, [])


    def createDatabase(self) -> None:
        """ Create a database specific for a show """
        print(f"============================== Database Created For {self.name} ==============================")
        self.database = {
            "name" : self.name ,
            "creator" : self.creator,
            "filePath" : self.filePath,    
            "producer" : self.producer,
            "director" : self.director 
        }
    
    def createAssociationsDatabase(self) -> None:
        """ Create an empty database.
        
        To be populated upon the creation of a show instance
        """
        self.database = {}

class Shot(DataManager): 
    """ Create a directory containing files related to a shot  """
    def __init__(self, filePath: str, shotNumber: int,FPS: float, lowerFrameRange: int, upperFrameRange: int, creator: str) -> None:
        self.shotNumber = shotNumber
        #self.assetAssociationsDB = assetAssociation
        self.FPS = FPS
        self.lowerFrameRange = lowerFrameRange
        self.upperFrameRange = upperFrameRange
        super().__init__(filePath, creator)


        print(f"============================== Added Show: {self.shotNumber} ============================== ")
    
        # this adds a particular instance of a shot as a key in the shot associations database so assets can be listed in it later
        self.updateAssociationsDatabase(self.shotAssociationsDB, f"Shot{self.shotNumber}", [])

    def createDatabase(self) -> None:
        """ Create a database specific for a shot """
        print(f"============================== Database Created For {self.name} ==============================")
        self.database = {
            "name" : self.name ,
            "creator" : self.creator,
            "filePath" : self.filePath,
            "shot number" : self.shotNumber,
            "asset association" : [],
            "frames per second" : self.FPS,
            "lower frame range" : self.lowerFrameRange,
            "upper frame range" : self.upperFrameRange,
            "characters in shot" : [],
            "assigned animators" : []   

        } 

class Asset(DataManager):
    """ Create a directory containing files related to an asset  """
    def __init__(self, filePath: str, category: str) -> None:
        self.name = self.getLastPathItem(filePath)
        self.category = category
        #self.shotAssociation = shotAssociation
        super().__init__(filePath)

        # this adds a particular instance of an asset as a key in the asset associations database so shots can be listed in it later
        self.updateAssociationsDatabase(self.assetAssociationsDB, self.name, [])

        # add asset to the category database
        self.addInDatabase(self.categoryAssociationsDB, category, self.name)

    def createDatabase(self) -> None:
        self.database = {
            "asset name" : self.name,
            "category" : self.category,
            "shot association" : []



        }
        



targetDirectory="C:/Users/jpark/Desktop/TestDirectory"
targetShow="C:/Users/jpark/Desktop/TestDirectory/Show1"
targetShot="C:/Users/jpark/Desktop/TestDirectory/Show1/Shot1"
targetDB="C:/Users/jpark/Desktop/TestDirectory/Show1/Shot0001/Shot1 DB"
targetAsset="C:/Users/jpark/Desktop/TestDirectory/Show1/Asset1"


tempDir=DirectoryOfShows(targetDirectory, "Assignee", "Creator1000",)
tempShow=Show(targetShow, "Producer99", "Director99", "Creator99")
tempShot=Shot(targetShot, 1, 23.97, 1, 40, "ArtistName")
tempShot=Shot("C:/Users/jpark/Desktop/TestDirectory/Show1/Shot2", 2, 23.97, 1, 40, "ArtistName")

# tempAsset=Asset(targetAsset, "character", [1,2], "Main Character Asset", "me") 
# tempAsset=Asset("C:/Users/jpark/Desktop/TestDirectory/Show1/Asset2", "character", [2], "Secondary Character Asset", "me") 
tempAsset=Asset(targetAsset, "character") 
tempAsset=Asset("C:/Users/jpark/Desktop/TestDirectory/Show1/Asset2", "character") 

tempAsset.associateAssetShot("Asset1", 1)
tempAsset.associateAssetShot("Asset2", 2)
tempAsset.associateAssetShot("Asset2", 1)
tempAsset.associateAssetShot("third asset", 2) 

# tempShow.archiveZip("Asset1")


# ** archive
tempShow.archiveZip("Asset1")
tempShot.archiveZip("Shot1")
# tempAsset.showArchiveContent("Asset1.zip")

tempAsset.showArchivedDatabase("Asset1")
tempShot.showArchivedDatabase("Shot1")

# tempShow.archiveZipShow("Show1")
# ** archive

