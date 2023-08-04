# Read Me

## About

In this second iteration of the project, added functionalities include the ability to archive files (zip), read from them, cateogrize assets and track associations between shots and assets. All previous functionalties remain.

## Getting Started

Refer to the `run_me.py ` to quickly generate an example with the latest module. 

### Create a Directory of Shows

Below is an example of how a user could get started:

``` python 

Dir1 = DirectoryOfShows(r"C:\Users\jpark\Desktop\TestDirectory", "Assignee", "Directory1", "Creator1", "DatabaseDOS")
Show1 = Show(r"C:\Users\jpark\Desktop\TestDirectory\Show1", "Producer1", "Director1", "Show1", "Creator2", "Show1 DB")
Shot1 = Shot(r"C:\Users\jpark\Desktop\TestDirectory\Show1\Shot0001", "Shot0001", "testshot", "Employee", "Shot001 DB")

class DirectoryOfShows(DataManager):
    def __init__(self, filePath, assigned, name, creator, databasename):
        self.assigned=assigned                                         
        super().__init__(filePath, name, creator, databasename) 

```
A user could use the first code block to get started. In the first argument, the user would input their own desired directory. The second code block is a reference for the DirectoryOfShows class initialization to show the parameters and their position. The difference for a Show is that you specify a producer and director of the show. In a shot, there are much more data fields that are technically specific.


filePath = The path in which you want to create this directory.<br> 
assigned = Name of the individual who is responsible for maintaining this directory<br>
name =  A name for this directory<br>
creator = Name of the individual who made this directory<br>
databasename = name of the json file that holds the directory's database

The user is able to create subsequent directories from the initial Dir1 instance using the `add_content()` method but that is not recommended. Doing so will only add a folder and not initialize a database in that directory. So, it is recommended that the user create a directory for Shows and Shots by calling their classes. The `add_content()` method is for general subdirectories that do not require a database.

While generating the first code block, the user could also set up multiple shows and shots:

```python
Dir1 = DirectoryOfShows(r"C:\Users\jpark\Desktop\TestDirectory", "Assignee", "Directory1", "Creator1", "DatabaseDOS")

Show1 = Show(r"C:\Users\jpark\Desktop\TestDirectory\Show1", "Producer1", "Director1", "Show1", "Creator2", "Show1 DB")
Show2 = Show(r"C:\Users\jpark\Desktop\TestDirectory\Show2", "Producer2", "Director2", "Show2", "Creator3", "Show2 DB")

Shot1 = Shot(r"C:\Users\jpark\Desktop\TestDirectory\Show1\Shot0001", "Shot0001", "testshot", "Employee", "Shot001 DB")
Shot2 = Shot(r"C:\Users\jpark\Desktop\TestDirectory\Show1\Shot0002", "Shot0002", "anothershot", "Employee", "Shot002 DB")

```

The user can confirm the directories by using the `get_content()` method:

```python
Dir1.get_content(r"C:\Users\jpark\Desktop\TestDirectory")


```

### Manage Directories

A user can come back at a later time and manage an existing directory. To do so they should call the `DataManager` parent class. This has only 1 required argument and that is the directory the user wants to manage: 


```python
DM = DataManager(r"C:\Users\jpark\Desktop\TestDirectory")


```

From this point, the user can review the directory and manage it:

```python

DM.add_content(r"C:\Users\jpark\Desktop\TestDirectory\Show1\Shot1\Subfolder1")
DM.move_file(r"some\file\from\elsewhere", r"C:\Users\jpark\Desktop\TestDirectory\Show1\Shot1\Subfolder1")

DM.showDatabase("Show1 DB")
DM.updateDatabase("Show1 DB", "frames per second", 23.97)
DM.showDatabase("Show1 DB")

```
Generally, the user should input the directory containing the shows as some methods, such as `showDatabase()` and `updateDatabase` search its directory and subdirectories for the given file and return its file path. 

The user can manage any database and directory within the initialized file path of a DataManager instance. 