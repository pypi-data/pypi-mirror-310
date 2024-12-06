# requirements_dev.txt we use for the testing
It makes it easier to install and manage dependencies for development and testing, separate from the dependencies required for production.

# difference between requirements_dev.txt and requirements.txt

requirements.txt is used to specify the dependencies required to run the production code of a Python project, while requirements_dev.txt is used to specify the dependencies required for development and testing purposes.

# tox.ini
We use if for the testing in the python package testing against different version of the python 

## how tox works tox enviornment creation
1. Install depedencies and packages 
2. Run commands
3. Its a combination of the (virtualenvwrapper and makefile)
4. It creates a .tox


# pyproject.toml
it is being used for configuration the python project it is a alternative of the setup.cfg file. its containts configuration related to the build system
such as the build tool used package name version author license and dependencies

# setup.cfg
In summary, setup.cfg is used by setuptools to configure the packaging and installation of a Python projec

# Testing python application
*types of testing*
1. Automated testing 
2. Manual testing

*Mode of testing*
1. Unit testing
2. Integration tests

*Testing frameworks*

1. pytest
2. unittest
3. robotframework
4. selenium
5. behave
6. doctest

# check with the code style formatting and syntax(coding standard)

1. pylint
2. flake8(it is best because it containt 3 library pylint pycodestyle mccabe)
3. pycodestyle


# How to use the package :-

### STEPS:-

```bash
pip install mongodb-crud-automation
```

```bash
from mongo_connect import mongo_crud
```

```bash
client_url = "<client_url_of_mongodb>"
database_name = "<database name>"
collection_name = "<collection_name>"
``` 

```bash
mongo = mongo_crud.mongodb_operation(client_url)
```

# CRUD Operation on MongoDB :-

## How to run :-

### 1. connected to the mongodb client database 

```bash
mongo.create_client()
```

### 2. create database in mongodb database 

```bash
mongo.create_database(database_name = "<database_name>")
```

### 3. create collection_name in mongodb database

```bash
mongo.create_collection(database_name= "<database_name>",
collection_name="<collection_name>")
```

### 4. insert single record 

```bash
mongo.insert_single_record(record:dict,database_name= "<database_name>",
collection_name="<collection_name>")
```

### 5. insert multiple records

```bash
mongo.insert_multiple_records([record:dict],database_name= "<database_name>" ,
collection_name="<collection_name>")
```

### 6. bulk insert record 
- in this datafile is in .csv or .xlsx file 

```bash
mongo.bulk_insert(datafile = "<file_path>",database_name= "<database_name>" ,
collection_name="<collection_name>",unique_field="<column_name>")
```

### 4. find query  
```bash
mongo.find(query: dict ={}, 
database_name= "<database_name>" ,collection_name="<collection_name>")
```

### 5. update query
```bash
mongo.update(query: dict = {} ,
new_values: dict = {},database_name= "<database_name>" ,collection_name="<collection_name>")
```

### 9. delete query
```bash
mongo.delete(query: dict = {} ,database_name= "<database_name>" ,   collection_name="<collection_name>")
```
