import os
import json
import shutil
from typing import Any

'test'
def dsdd():
    pass

class DataManager:
    def __init__(self, filePath: str, name="default name", creator="default creator name", databasename="default database") -> None: 
        self.name = name
        self.creator = creator
        self.filePath = filePath
        self.databasename = databasename
        self.databasePath = None 
        
        path=os.path.join(self.filePath) # if only 1 argument, useful for turning \ into /

        if os.path.exists(path) == True:
            print(f"Current Directory Set To: {self.filePath}")
        else:
            print("============================== Updated Directory ============================== ")
            print(f"Added directory: {path}")
            os.makedirs(path)

            self.createDatabase(databasename)
            self.writeDatabase(self.databasename)

    def makePath(self,*pathargs: str) -> str:
       # if pathargs contains self.filePath in it, it will still work. seems like os.path.join will be smart and not duplicate a part of the path
       path=os.path.join(self.filePath, "/".join(pathargs))
       print(f"makepath: {path}")
       return path

    def createDatabase(self, databasename: str) -> None:
        self.database=databasename
        print(f"============================== Database Created For {self.name}: {self.databasename} ==============================")
        self.database = {
            "database name" : self.databasename,
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
    
    def showDatabase(self, targetDB: str) -> None:   

        with open(self.getFilePath(targetDB, self.filePath),'r') as file:
            print(file.read())


    def updateDatabase(self, targetDB: str, key: str, value: Any) -> None:

        with open(self.getFilePath(targetDB, self.filePath), "r") as file:
            tempDatabase = json.load(file)

        tempDatabase[key]=value

        print(f"**** Updated Database: {key} : {value} ****")

        with open(self.getFilePath(targetDB, self.filePath),'w') as file:
            json.dump(tempDatabase, file, indent=4)

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

class DirectoryOfShows(DataManager):
    def __init__(self, filePath: str, assigned: str, name: str, creator: str, databasename: str) -> None:
        self.assigned = assigned                                                 # <-- this needs to come before super()....or else line 152 will error; if super before, 
        super().__init__(filePath, name, creator, databasename)                     # it will run createDatabase (go to parent class, and see a more specific one in child class) 
                                                                                    # before it gets to read self.assigned=assigned
    
    def createDatabase(self, databasename: str) -> None:
        self.database = databasename
        print(f"============================== Database Created For {self.name}: {self.databasename} ==============================")
        self.database = {
            "name" : self.name ,
            "creator" : self.creator,
            "filePath" : self.filePath,
            "assigned" : self.assigned,     
        }


class Show(DataManager):
    def __init__(self, filePath: str, producer: str, director: str, name: str, creator: str, databasename: str) -> None:
        self.producer = producer
        self.director = director
        super().__init__(filePath, name, creator, databasename)


        print(f"============================== Added Show: {self.name} ============================== ")

        self.createAssociationsDatabase()
        self.writeDatabase("Asset and Shot Associations")

    def createDatabase(self, databasename: str) -> None:
        self.database=databasename
        print(f"============================== Database Created For {self.name}: {self.databasename} ==============================")
        self.database = {
            "database name" : self.databasename,
            "name" : self.name ,
            "creator" : self.creator,
            "filePath" : self.filePath,    
            "producer" : self.producer,
            "director" : self.director 
        }
    
    def createAssociationsDatabase(self) -> None:
        self.database = {
            "database name" : self.databasename + " - Associations Database"
        }

class Shot(DataManager): 
    def __init__(self, filePath: str, shotNumber: int, FPS: float, lowerFrameRange: int, upperFrameRange: int, name: str, creator: str, databasename: str) -> None:
        self.shotNumber = shotNumber
        self.FPS = FPS
        self.lowerFrameRange = lowerFrameRange
        self.upperFrameRange = upperFrameRange
        super().__init__(filePath, name, creator, databasename)

        print(f"============================== Added Show: {self.shotNumber} ============================== ")
    


        self.updateDatabase("Asset and Shot Associations", f"shot number {self.shotNumber}", [])


    def updateDatabase(self, targetDB: str, key: str, value: Any) -> None:
        # this method is modified from the parent class to specifically suit the creation of the Asset and Shot Associations json file
        # this is different as it needs to access the json file in its parent directory; if not for this modification, the method in the
        # parent class would look for the json file in the Shot directory and not the Show directory


        parent_directory = os.path.dirname(self.filePath)
        associationsDB = parent_directory + "/" + targetDB

        with open(associationsDB, "r") as file:
            tempDatabase = json.load(file)

        tempDatabase[key]=value

        print(f"**** Updated Database: {key} : {value} ****")

        with open(associationsDB,'w') as file:
            json.dump(tempDatabase, file, indent=4)


    def createDatabase(self, databasename: str) -> None:
        self.database=databasename
        print(f"============================== Database Created For {self.name}: {self.databasename} ==============================")
        self.database = {
            "database name" : self.databasename,
            "name" : self.name ,
            "creator" : self.creator,
            "filePath" : self.filePath,
            "shot number" : self.shotNumber,
            "frames per second" : self.FPS,
            "lower frame range" : self.lowerFrameRange,
            "upper frame range" : self.upperFrameRange,
            "characters in shot" : [],
            "assigned animators" : []   

        } 


targetDirectory="C:/Users/jpark/Desktop/TestDirectory"
targetShow="C:/Users/jpark/Desktop/TestDirectory/Show1"
targetShot="C:/Users/jpark/Desktop/TestDirectory/Show1/Shot0001"
targetDB="C:/Users/jpark/Desktop/TestDirectory/Show1/Shot0001/Shot1 DB"


tempDir=DirectoryOfShows(targetDirectory, "Assignee", "Directory1", "Creator1000", "Directory1 DB")
tempShow=Show(targetShow, "Producer99", "Director99", "Show1", "Creator99", "Show1 DB")
tempShot=Shot(targetShot, 1, 23.97, 1, 40, "testshot", "ArtistName", "Shot1 DB") 