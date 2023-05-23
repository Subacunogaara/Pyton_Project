# Project Title
MySQL Database with Repository Pattern and OOP

## Description
This project includes scripts to load data from JSON files into a MySQL database and execute queries on that database. The `filling_database.py` script reads from JSON files and writes to an already created database with tables with the following schemes:

### rooms

| Field | Type | Null | Key | Default | Extra |
| ----- | ---- | ---- | --- | ------- | ----- |
| id | int | NO | PRI | NULL | |
| name | varchar(50) | YES | | NULL | |

### students

| Field | Type | Null | Key | Default | Extra |
| ----- | ---- | ---- | --- | ------- | ----- |
| id | int | NO | PRI | NULL | |
| name | varchar(50) | YES | | NULL | |
| birthday | date | YES | | NULL | |
| sex | enum('M','F') | YES | | NULL | |
| room | int | YES | MUL | NULL | |

The `db_repository.py` script is based on the "Repository" pattern and OOP. Instances of the `RoomRepository` class can connect to the database and contain the following methods for querying the database:

* `get_rooms_with_num_students` - returns a list of rooms and the number of students in each room
* `get_rooms_with_min_avg_age` - returns 5 rooms with the smallest average age of students (the default value is 5, but you can pass any integer to the limit parameter)
* `get_rooms_with_age_diff` - returns 5 rooms with the largest age difference between students (the default value is 5, but any integer can be passed to the limit parameter)
* `get_rooms_with_diff_genders` - returns the list of rooms where different-sex students live

All results are returned in JSON format.

## Getting Started
To use the scripts, clone the repository and install the necessary dependencies by running `pip install -r requirements.txt`.

## Usage
To fill the database with data from JSON files, run the `filling_database.py` script. To query the database, create an instance of the `RoomRepository` class and use its methods.