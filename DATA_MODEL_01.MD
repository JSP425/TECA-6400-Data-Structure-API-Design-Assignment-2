# Data Model Explanation

In this project, my data model is designed to manage directories for a hypothetical production. The data model relies on a parent class titled `DataManager` and the child classes `DirectoryofShows`, `Show`, and `Shots`.

## Design Rationale

While reviewing the requirements for the Python library, I noticed that each level of directory required much of the same functionality. For example, a directory **containing shows** requires the ability to add/remove subdirectories (shows) in the same way a directory **inside of a show** needs to do the same with subdirectories of shots.

I view each directory level to be essentially the same except for their names, filepaths and some specific data fields about them. For example, there may be an assigned individual to manage a Directory of Shows whereas there may be a producer/director managing a particular show. So, I created the DataManager parent class to encapsulate common functionalities as methods; the child classes inherit from these base functionalities but can overwrite them for their own specific instances. This will make the code reusable and easier to maintain.

Ultimately, there is an 'is-a' relationship between the DataManager and its child classes. All the child classes are just a more specific version of a general DataManager. The difference between the instances are in the contents of the database.

So, when a child class is instantiated, a database in the form of a json file is automatically created in the initialized directory. In the json file is a dictionary containing data specific to the instantiated directory. 

In terms of the parent class DataManager, an instance of it could be used to create a general directory and that would come with a generic database with default values. This is what would result if you call this class with a file path that did not exist previously. If you input a file path that does exist, the class will not create that directory or a corresponding database; rather, it will just acknowledge that this path exists and leave the user with an instance they can access the file management methods. For convenience, I put default values for all the parameters in this class except for the file path so the user only needs to specify the directory they want to work in. Typically, the DataManager parent class should be initialized to manage an existing directory.

As the child classes are differentiated from one another by the contents of their json database, these child classes have required arguments in their initialization that correspond to those fields. 

## Other Data Types

The most common data type in this data model are strings; they are necessary for the user to input file paths and to populate data fields. Most of the data collected will be in string form as the fields are typically qualitative: names of productions, shows, files and people.

Dictionaries are used to maintain the database concerning the current directory. This will allow the user to easily view and modify data fields. 

Integers are used for quantitative data fields such as dates, shot numbers and frame ranges. The data collected for these fields may be useful for future calculations so it is preferred that they are of a numeric type. These fields' values are not fractional and should be integers whereas FPS is a float.

Lists are used in the database for shots to list 'characters in shot' and 'assigned animators'.

Booleans were used to check if a file path already exists and to prompt the user accordingly.

None types are set in the parent class initialization of variables; this is for cleaner coding purposes so all variables can be identified at the start of the module and so that they are not initialzied later on; this also allows for easier de-bugging/error tracking. 

## General Folder Structure

Project 1 is the root folder. Inside it is the PipelineLibrary_V1.py which is the module and a tests folder containing test_PipelineTest.py. which tests the module via pytest. Inside the root folder are also the READ_Me.md and the DATA_MODEL.md.


## Parent Class: DataManager

The `DataManager` class serves as the base class and contains common attributes and methods for managing directories. Here are the key elements of the `DataManager` class:

- **Attributes**:
  - `name`: Represents the name of the data manager instance.
  - `creator`: Represents the creator of the data manager instance.
  - `filePath`: Represents the file path for the directory.
  - `databasename`: Represents the name of the database associated with the directory.
  - `databasePath`: Stores the file path of the database (initially set to `None`).

- **Methods**:
  - `makePath()`: Takes path arguments and returns the combined path by joining them.
  - `createDatabase()`: Creates the database dictionary for the directory.
  - `write_database()`: Writes the database dictionary to a JSON file.
  - `get_filePath()` : Takes a file name argument and a directory to search and return the file's full file path. 
  - `showDatabase()`: Displays the content of the database file.
  - `updateDatabase()`: Updates a specific key-value pair in the database.
  - `add_content()`: Creates a new directory at the specified path.
  - `get_content()`: Retrieves and displays the contents of a specific directory.
  - `move_file()`: Moves a file from the source path to the destination path.
  - `remove_file()`: Removes a file from the specified path.
  - `remove_folder()`: Removes a folder and its contents from the specified path.

## Child Classes: DirectoryOfShows, Show, Shot

The child classes inherit from the `DataManager` class and represent more specific types of directories. Here's a brief explanation of each child class:

- **DirectoryOfShows**:
  - Inherits from `DataManager`.
  - Additional attribute: `assigned`, representing the assigned individual to manage the directory.
  - Overrides the `createDatabase()` method to include the `assigned` attribute in the database dictionary.

- **Show**:
  - Inherits from `DataManager`.
  - Additional attributes: `producer` and `director`, representing the producer and director of the show.
  - Overrides the `createDatabase()` method to include the `producer` and `director` attributes in the database dictionary.

- **Shot**:
  - Inherits from `DataManager`.
  - Additional attribute: `shotNumber`, `FPS`, `lowerFrameRange`, `upperFrameRange` representing the shot number, frames per second and the frame range respectively.
  - Overrides the `createDatabase()` method to include the new attributes described above in the database dictionary.


