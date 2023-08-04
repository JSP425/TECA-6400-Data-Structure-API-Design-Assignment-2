# Data Model Explanation

In this project, my data model is designed to manage directories for a hypothetical production. The data model relies on a parent class titled `DataManager` and the child classes `DirectoryofShows`, `Show`,`Shots` and `Assets`.

## Design Rationale

While reviewing the requirements for the Python library, I noticed that each level of directory required much of the same functionality. For example, a directory containing shows requires the ability to add/remove subdirectories (shows) in the same way a directory inside of a show needs to with subdirectories of shots.

I view each directory level to be essentially the same except for their names, filepaths and some specific data fields about them. For example, there may be an assigned individual to manage a Directory of Shows whereas there may be a producer/director managing a particular show. So, I created the DataManager parent class to encapsulate common functionalities as methods; the child classes inherit from these base functionalities but can overwrite them for their own specific instances. This will make the code reusable and easier to maintain.

Ultimately, there is an 'is-a' relationship between the DataManager and its child classes. All the child classes are just a more specific version of a general DataManager. The difference between the instances are in the contents of the database.

So, when a child class is instantiated, a database in the form of a json file is automatically created in the initialized directory. In the json file is a dictionary containing data specific to the instantiated directory.

In terms of the parent class DataManager, an instance of it could be used to create a general directory without prepopulated databases. This is what results if you call this class with a file path that did not exist previously. If you input a file path that does exist, the class will not create that directory or a corresponding database; rather, it will just acknowledge that this path exists and leave the user with an instance they can access the file management methods. For convenience, I put default values for all the parameters in this class except for the file path so the user only needs to specify the directory they want to work in. Typically, the DataManager parent class should be initialized to manage an existing directory.

As the child classes are differentiated from one another by the contents of their json database, these child classes have required arguments in their initialization that correspond to those fields.

## Design Differences from Project 1

Changes have been made to the previous data model to accommodate the requirements for Project 2 and for overall efficiency.

Most notably, many methods in the parent class that utilized the `get_filePath()` method have been replaced with `getFilePathFromParent()`. This also returns the file path of a targeted file but the latter begins it search from the parent directory rather than the instanced directory (`self.filePath`).  This method was created so that an asset or shot instance could access databases at the show level.

Those databases at the show level are `Shot-Asset Associations Database`, `Asset-Shot Associations Database`, `Assets by Categories Database` and `Asset List`. These databases detail which assets and shots are associated to one another and which assets belong to what category. Although this data is also available in the databases specific to each asset and shot, I decided I wanted to compile this information in dedicated databases for easier future access; doing so would be more efficient and less complex than having to loop through the various directories, pulling out relevent data, compiling a new list and printing it.

In this design, an instantiation of a show automatically creates these databases at the show level directory. An instantiation of an asset or shot will add themselves to the appropriate databases. For example, the creation of `Asset1` will create its own directory and in it `Asset1 Database`; however it will also add `Asset1` to `Asset-Shot Associations Database` as the first key with a value of `[]`. In this empty list shots can be appended. When a user wants to make associations they use the `associateAssetShot()` method as it will update the asset and shot specific databases and the overarching databases at the show level. This way, the databases stay in sync. 

So, to accomodate the need to reach the databases at the show level, `getFilePathFromParent()` became the successor; as it is essentially the same as its predecessor, there were few issues in its implementation. An issue did arise when there were mutliple shows and the module would satisfy its search for the overarching databases for the second show in the first show (as it started its search from parent directory of shows). 

For this reason, a few methods still utilize `get_filePath()` and the decision was made to recommend to the user to instantiate the DataManager parent class with the specific directory they want to manage. In the previous model, the user was able to instance the DataManager class at the root directory level and manage any level within it. 

### Other Changes

The `name` parameter for classes have been removed. It was redundant and caused confusion as the name of the directory was captured when providing the file path. Now the module automatically assigns the `self.name` attribute based on the given file path. To simplify the instantiating process, the `databasename` parameters were also removed and will databases will automatically be named according `self.name` + `" Database"`. This was preferred as it also made the retrieval of databases easier.

The methods within the parent class have been reorganized by grouping within the following headings: `Path Manipulating Methods`, `Database Methods`,`Data Retrieval Methods` and `File/Directory Methods`. Putting the classess and methods in separate files/modules would have been preferred.

Some previous methods were renamed mostly to be consistent with the majority of other functions being written in camel casing. 

## Other Data Types

The data model employs various data types to handle different aspects of the production data:

1. Strings: Strings are commonly used for inputting file paths, names of productions, shows, files, and people, as most of the data collected is qualitative in nature.

2. Dictionaries: Dictionaries are utilized to maintain databases containing data specific to each directory. They enable easy viewing and modification of data fields.

3. Integers: Integers are used for quantitative data fields such as dates, shot numbers, and frame ranges. Numeric data is preferred for potential future calculations, and these fields do not require fractional values.

4. Lists: Lists are used within the database for the 'characters in shot' and 'assigned animators' fields, allowing multiple entries for associated data.

5. Booleans: Booleans are used to check whether a file path already exists, guiding the user accordingly.

6. None Type: Variables in the `DataManager` parent class are initialized with None type for cleaner coding and easier debugging/error tracking.

## General Folder Structure

The root folder is named `Project 2,` containing the main module `project2pipeline.py`. There is also a `tests` folder containing `test_pipeline.py`, which is used for pytest testing and a `confest.py` that sets up pytest fixtures. Additionally, the root folder holds `read_me.md` and `data_model.md` for project documentation. Included is a `run_me.py` which will quickly generate example directories using the `project2pipeline.py` module. A virtual environment was set up to locally install pytest.

## Parent Class: DataManager

The `DataManager` class serves as the base class and encompasses common attributes and methods for managing directories. Key elements of the `DataManager` class include:


## Child Classes: DirectoryOfShows, Show, Shot, Asset

The child classes inherit from the `DataManager` class and represent more specific types of directories. Here's a brief explanation of each child class:

### DirectoryOfShows:
- Inherits from `DataManager`.
- Additional attribute: `assigned`, representing the assigned individual to manage the directory.
- Overrides the `createDatabase()` method to include the `assigned` attribute in the database dictionary.

### Show:
- Inherits from `DataManager`.
- Additional attributes: `producer` and `director`, representing the producer and director of the show.
- Overrides the `createDatabase()` method to include the `producer` and `director` attributes in the database dictionary.

### Shot:
- Inherits from `DataManager`.
- Additional attributes: `shotNumber`, `FPS`, `lowerFrameRange`, and `upperFrameRange`, representing the shot number, frames per second, and frame range, respectively.
- Overrides the `createDatabase()` method to include the new attributes in the database dictionary.

Apologies for the oversight. Here is the information about the `Asset` child class:

### Asset
- Inherits from `DataManager`.
- Additional attribute: `category`, representing the category of the asset (e.g., character, prop, environment).
- Overrides the `createDatabase()` method to include the `category` attribute in the database dictionary.
- Upon creation, it adds the asset as a key to the "Asset-Shot Associations Database" with an empty list for shot associations.
- It appends the asset to the "Assets by Categories Database" under its respective category.
- It also adds the asset to the "Asset List" database.
