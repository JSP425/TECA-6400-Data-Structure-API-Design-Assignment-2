import os
import json
import shutil
import zipfile
from typing import Any


"will need to load a target directory vs the highlest when creating data manager class as associations DB will all have same name within each show"
class DataManager:
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
       # if pathargs contains self.filePath in it, it will still work. seems like os.path.join will be smart and not duplicate a part of the path
       path=os.path.join(self.filePath, "/".join(pathargs))
       print(f"makepath: {path}")
       return path

    def getFilePath(self, file_name: str, directory_path: str) -> str:
        # this function is for conveniently getting the file path for a database json file
        # this will allow the user to just type in the database name in the methods below to see/manage its content
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
        # this function is for conveniently getting the file path for a database json file
        # this will allow the user to just type in the database name in the methods below to see/manage its content
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

    def getLastPathItem(self, targetPath: str) -> None:
        result = os.path.basename(targetPath)
        return result
        
    def getDirectoryPath(self, directory_name: str, directory_path: str) -> str:
        # this function is for conveniently getting the file path for a database json file
        # this will allow the user to just type in the database name in the methods below to see/manage its content
        for root, dirs, files in os.walk(directory_path):
            if directory_name in dirs:
                target_path = os.path.join(root, directory_name)
                print("File found at:", target_path)
                return target_path

        # File not found
        else:
            print(f"Directory {directory_name} not found inside {directory_path}.")
            return None

    def checkExist(self, folderName: str) -> None:
        parent_directory = os.path.dirname(self.filePath)
        # print(f"********parent_directory**********{parent_directory}")
        # print(f"******targetPath******{targetPath}")
        targetExist = self.getDirectoryPath(folderName, parent_directory)
        # print(f"********targetexistdb**********{targetExistDB}")

        # if targetExistDB:
        #     result=os.path.exists(targetExistDB)
        #     return result
        # else:
        #     return False

        if targetExist == None:
            return False
        else:
            result=os.path.exists(targetExist)
            return result    

        
    # ======================================================== Database Methods ================================================
    def createDatabase(self) -> None:
        #self.database=databasename
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
        print("============================== Created JSON File ==============================")
        self.databasePath=self.makePath(*args)
        with open(self.databasePath,'w') as file:
            json.dump(self.database, file, indent=4)
        print(f"added a file at {self.databasePath}")

    
    def updateDatabase(self, targetDB: str, key: str, value: Any) -> None:

        with open(self.getFilePathFromParent(targetDB, self.filePath), "r") as file:
            tempDatabase = json.load(file)

        tempDatabase[key]=value

        print(f"**** Updated Database: {key} : {value} ****")

        with open(self.getFilePathFromParent(targetDB, self.filePath),'w') as file:
            json.dump(tempDatabase, file, indent=4)

    def updateAssociationsDatabase(self, targetDB: str, key: str, value: Any) -> None:
        # this method is modified from the parent class to specifically suit the creation of the Asset and Shot Associations json file
        # this is different as it needs to access the json file in its parent directory; if not for this modification, the method in the
        # parent class would look for the json file in the Shot directory and not the Show directory, returning a type error of None


        # parent_directory = os.path.dirname(self.filePath)

        # associationsDB = self.getFilePath(targetDB, parent_directory)
        associationsDB = self.getFilePathFromParent(targetDB, self.filePath)

        with open(associationsDB, "r") as file:
            tempDatabase = json.load(file)

        tempDatabase[key]=value

        print(f"**** Updated Database: {key} : {value} ****")

        with open(associationsDB,'w') as file:
            json.dump(tempDatabase, file, indent=4)
     

    def addInDatabase(self, targetDB: str, key: str, value: Any) -> None:

        associationsDB = self.getFilePathFromParent(targetDB, self.filePath)

        with open(associationsDB, "r") as file:
            tempDatabase = json.load(file)
        
        tempDatabase[key].append(value)

        print(f"**** Updated Database: {key} : {value} ****")

        with open(associationsDB,'w') as file:
            json.dump(tempDatabase, file, indent=4)
    
        
    def associateAssetShot(self, assetName: str, shotNumber: int) -> None:
        assetNamePath=self.checkExist(assetName)
        #print(f"************************asset name path {assetNamePath}")

        shotNumberPath=self.checkExist(f"Shot{shotNumber}")
        #print(f"************************shotNumber {shotNumber}")

        if assetNamePath and shotNumberPath:
            self.addInDatabase(assetName + " Database", "shot association", shotNumber)
            self.addInDatabase("Shot" + str(shotNumber) + " Database", "asset association", assetName)


            self.addInDatabase(self.assetAssociationsDB, assetName, shotNumber)
            self.addInDatabase(self.shotAssociationsDB, f"Shot{shotNumber}", assetName)

        else:
            if not assetNamePath:
                print(f"The asset '{assetName}' does not exist. Association not made. Please double-check.")
            if not shotNumberPath:
                print(f"The shot 'Shot{shotNumber}' does not exist. Association not made. Please double-check.")
    
    # ======================================================== Retrieve Data Methods ================================================

    def showDatabase(self, targetDB: str) -> None:   
        with open(self.getFilePathFromParent(targetDB, self.filePath),'r') as file:
            print(file.read())

    def showDatabaseKey(self, targetDB: str, key: str) -> dict:
        # with open(self.getFilePath(targetDB, self.filePath),'r') as file:
        with open(self.getFilePathFromParent(targetDB, self.filePath),'r') as file:
            jsonData=json.load(file)

            value = jsonData.get(key, "Key not found")

            return value

    def showShotAssociationFor(self, assetName: str) -> dict:
        with open(self.getFilePathFromParent(assetName + " Database", self.filePath),'r') as file:
            jsonData=json.load(file)

            value = jsonData.get("shot association", "Key not found")

            return value
        
    def showAssetAssociationFor(self, shotNumber: int) -> dict:
        with open(self.getFilePathFromParent("Shot" + str(shotNumber) + " Database", self.filePath),'r') as file:
            jsonData=json.load(file)

            value = jsonData.get("asset association", "Key not found")

            return value
        
    def showADBforAssetKey(self, key: str) -> None:
        with open(self.getFilePathFromParent(self.assetAssociationsDB, self.filePath),'r') as file:
            jsonData=json.load(file)

            value = jsonData.get(key, "Key not found")

            return value
        
    def showADBforShotKey(self, key: str) -> None:
        with open(self.getFilePathFromParent(self.shotAssociationsDB, self.filePath),'r') as file:
            jsonData=json.load(file)

            value = jsonData.get("Shot"+str(key), "Key not found")

            return value
        
    def showCharacterCategory(self) -> None:
        with open(self.getFilePathFromParent(self.categoryAssociationsDB, self.filePath),'r') as file:
            jsonData=json.load(file)

            value = jsonData.get("character", "Key not found")

            return value
    
    def showPropCategory(self) -> None:
        with open(self.getFilePathFromParent(self.categoryAssociationsDB, self.filePath),'r') as file:
            jsonData=json.load(file)

            value = jsonData.get("prop", "Key not found")

            return value
    
    def showEnvironmentCategory(self) -> None:
        with open(self.getFilePathFromParent(self.categoryAssociationsDB, self.filePath),'r') as file:
            jsonData=json.load(file)

            value = jsonData.get("environment", "Key not found")

            return value
        
    def showArchiveContent(self, folderName: str) -> list:
        # get filepathfromparent b/c folder name will be a zip FILE
        targetPath=self.getFilePathFromParent(folderName, self.filePath)
        with zipfile.ZipFile(targetPath, "r") as zipTarget:
            zipContent=zipTarget.namelist()

            for eachItem in zipContent:
                print(eachItem)
            return zipContent
        
    def showArchivedDatabase(self, targetName):

        zipFileName=targetName+".zip"
        zipFilePath=self.getFilePathFromParent(zipFileName, self.filePath)
        #print(f"+*+*+*+*+*+*+* zipfilepath = {zipFilePath}")

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
        print(f"============================== Added: {self.name} ============================== ")
        newpath=self.makePath(*args)

        if os.path.exists(newpath) == True:
            print("This file path already exists")
        else:
            print(f"Added show: {newpath}")
            os.makedirs(newpath)

    def getContent(self, *args: str) -> None:
        print(f"============================== Content: {self.name} ==============================")
        newpath=self.makePath(*args)

        contents=os.listdir(newpath)
        print(f"Contents of {newpath}: \n {contents}")
    
    def moveFile(self, sourcePath: str, destinationPath: str) -> None:

        if os.path.exists(destinationPath):
            shutil.move(sourcePath,destinationPath)
        else:
            print("Invalid destination directory")
        
    def removeFile(self,*args: str) -> None:
        print(f"============================== Updated: {self.name} ============================== ")
        newpath=self.makePath(*args)
        if os.path.exists(newpath):
            os.remove(newpath)
            print(f"{newpath} was removed")
        else:
            print("File does not exist.")
    
    def removeFolder(self, *args: str) -> None:
        print(f"============================== Updated: {self.name} ============================== ")
        newpath=self.makePath(*args)
        #path=os.path.join(self.filePath, "/".join(args))
        shutil.rmtree(newpath)    
        print(f"removed a directory and its contents at {newpath}")

    # def archiveZipFile(self, folderName: str) -> None:
    #     folderPath=self.checkExist(folderName)
        
    #     if folderPath: 
    #         targetPath=self.getDirectoryPathFromParent(folderName, self.filePath)
    #         print(f"*+*+*+*+*+*+*+*+target path of zip{targetPath}")
    #         with zipfile.ZipFile(targetPath, 'w', zipfile.ZIP_DEFLATED) as zipRef:
    #             #zip_ref.extractall()
    #             zipRef.write(folderPath)
            
    #         os.remove(targetPath)

    #     else:
    #         print(f"Unable to ZIP directory {folderName} as it does not exist.")

    def archiveZip(self, folderName):
        
        targetPath=self.getDirectoryPathFromParent(folderName, self.filePath)
        parentPath = os.path.dirname(targetPath)
        shutil.make_archive(targetPath, 'zip', parentPath, folderName)
        #os.remove(targetPath)
        self.removeFolder(targetPath)

        # need to ask ryan about how this shutil method works; review documentation with him
        # my guess: targetPath = base name is where zip will be (if path not specified, relative to directory where script is?)
        # parentPath = root dir wants to know where the folder i want to zip is...so the parent directory
        # folderName = base dir wants to know which directory in root dir to zip...so give it the name of the existing directory?

    def archiveZipAll(self, showName):
        targetPath=self.getDirectoryPathFromParent(showName, self.filePath)
        for each in os.listdir(targetPath):
            subDirPath=os.path.join(targetPath,each)
            if os.path.isdir(subDirPath) == True:
                shutil.make_archive(subDirPath,'zip',self.filePath, each)
                self.removeFolder(subDirPath)




class DirectoryOfShows(DataManager):
    def __init__(self, filePath: str, assigned: str, creator: str) -> None:
        self.assigned = assigned                                                 # <-- this needs to come before super()....or else line 152 will error; if super before, 
        super().__init__(filePath, creator)                                   # it will run createDatabase (go to parent class, and see a more specific one in child class) 
                                                                                    # before it gets to read self.assigned=assigned
    
    def createDatabase(self) -> None:
        print(f"============================== Database Created For {self.name} ==============================")
        self.database = {
            "name" : self.name ,
            "creator" : self.creator,
            "filePath" : self.filePath,
            "assigned" : self.assigned,     
        }


class Show(DataManager):
    def __init__(self, filePath: str, producer: str, director: str, creator: str) -> None:
        self.producer = producer
        self.director = director
        super().__init__(filePath, creator)



        print(f"============================== Added Show: {self.name} ============================== ")

        self.createAssociationsDatabase()
        self.writeDatabase(self.shotAssociationsDB)
        self.writeDatabase(self.assetAssociationsDB)
        self.writeDatabase(self.categoryAssociationsDB)

        # self.updateDatabase(self.categoryAssociationsDB, "character", [])
        self.updateAssociationsDatabase(self.categoryAssociationsDB, self.categoryCharacterKey, [])
        self.updateAssociationsDatabase(self.categoryAssociationsDB, self.categoryPropKey, [])
        self.updateAssociationsDatabase(self.categoryAssociationsDB, self.categoryEnvironmentKey, [])


    def createDatabase(self) -> None:
        print(f"============================== Database Created For {self.name} ==============================")
        self.database = {
            "name" : self.name ,
            "creator" : self.creator,
            "filePath" : self.filePath,    
            "producer" : self.producer,
            "director" : self.director 
        }
    
    def createAssociationsDatabase(self) -> None:
        self.database = {}

class Shot(DataManager): 
    def __init__(self, filePath: str, shotNumber: int,FPS: float, lowerFrameRange: int, upperFrameRange: int, creator: str) -> None:
        self.shotNumber = shotNumber
        #self.assetAssociationsDB = assetAssociation
        self.FPS = FPS
        self.lowerFrameRange = lowerFrameRange
        self.upperFrameRange = upperFrameRange
        super().__init__(filePath, creator)


        print(f"============================== Added Show: {self.shotNumber} ============================== ")
    

        self.updateAssociationsDatabase(self.shotAssociationsDB, f"Shot{self.shotNumber}", [])

    def createDatabase(self) -> None:
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
    def __init__(self, filePath: str, category: str) -> None:
        self.name = self.getLastPathItem(filePath)
        self.category = category
        #self.shotAssociation = shotAssociation
        super().__init__(filePath)

        # add asset name to list of assets associated with shots
        self.updateAssociationsDatabase(self.assetAssociationsDB, self.name, [])

        # add asset to category DB
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

tempShow.archiveZip("Asset1")
tempAsset.showArchiveContent("Asset1.zip")

tempAsset.showArchivedDatabase("Asset1")
tempShow.archiveZipAll("Show1")