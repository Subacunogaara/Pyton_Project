import json
import mysql.connector as connection
import os
from datetime import datetime
import pytest


password = os.environ.get('PASSWORD_FOR_PYTHON_INTRO')
user = os.environ.get('USER_FOR_PYTHON_INTRO')
host = os.environ.get('HOST_FOR_PYTHON_INTRO')
database_name = os.environ.get('DATABASE_FOR_PYTHON_INTRO')

def test_rooms_table_is_populated():
    connect_to_db = connection.connect(user=user,
                                       password=password,
                                       host=host,
                                       database=database_name)
    cursor = connect_to_db.cursor()
    cursor.execute('SELECT COUNT(*) FROM rooms')
    result = cursor.fetchone()[0] # we need first value from tuple
    cursor.close()
    connect_to_db.close()
    assert result > 0

def test_students_table_is_populated():
    connect_to_db = connection.connect(user=user,
                                       password=password,
                                       host=host,
                                       database=database_name)
    cursor = connect_to_db.cursor()
    cursor.execute('SELECT COUNT(*) FROM students')
    result = cursor.fetchone()[0]  # we need first value from tuple
    cursor.close()
    connect_to_db.close()
    assert result > 0

def test_insert_data_is_correct():
    connect_to_db = connection.connect(user=user,
                                       password=password,
                                       host=host,
                                       database=database_name)
    cursor = connect_to_db.cursor()
    cursor.execute('SELECT COUNT(*) FROM rooms')
    number_of_rooms = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM students')
    number_of_students = cursor.fetchone()[0]
    cursor.execute('SELECT rooms.name, COUNT(rooms.id) '
                   'FROM rooms LEFT JOIN students ON rooms.id=students.room '
                   'GROUP BY rooms.name')
    result = cursor.fetchall()
    cursor.close()
    assert len(result) == number_of_rooms, \
        f"Number of rooms in query ({len(result)}) differs from actual number of rooms ({number_of_rooms})"
    assert all(count > 0 for name, count in result), f"At least one room in query ({result}) is empty"
    assert all(count <= number_of_students for name, count in result), \
        f"Number of students in some rooms in query is greater than total number of students ({result})"

    # Check that all rooms have correct names and unique IDs
    with open('/home/user/Traning_Projects/1_Python_Introduction/rooms.json', 'r') as file:
        rooms_from_file = json.load(file)
    rooms_from_db = {}
    cursor = connect_to_db.cursor()
    cursor.execute('SELECT id, name FROM rooms')
    for row in cursor.fetchall():
        room_id = row[0]
        room_name = row[1]
        assert room_id not in rooms_from_db, f"Duplicate room ID in the database: {room_id}"
        assert room_name, f"Room with ID {room_id} has an empty name"
        rooms_from_db[room_id] = room_name
    cursor.close()
    assert len(rooms_from_db) == number_of_rooms, \
        f"Number of rooms in the database ({len(rooms_from_db)}) differs from the actual number of rooms ({number_of_rooms})"
    for room in rooms_from_file:
        assert room['id'] in rooms_from_db, f"Room with ID {room['id']} from JSON file is not found in the database"
        assert rooms_from_db[room['id']] == room['name'], \
            f"Room with ID {room['id']} in the database has a different name than in the JSON file"

    # Check that all students have correct data and unique IDs
    with open('/home/user/Traning_Projects/1_Python_Introduction/students.json', 'r') as file:
        students_from_file = json.load(file)
    students_from_db = {}
    cursor = connect_to_db.cursor()
    cursor.execute('SELECT id, name, birthday, sex, room FROM students')
    for row in cursor.fetchall():
        student_id = row[0]
        student_name = row[1]
        student_birthday = datetime.strptime(str(row[2]) + ' 00:00:00', '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S.%f')
        student_sex = row[3]
        student_room = row[4]
        assert student_id not in students_from_db, f"Duplicate student ID in the database: {student_id}"
        assert student_name, f"Student with ID {student_id} has an empty name"
        assert student_birthday, f"Student with ID {student_id} has an empty birthday"
        assert student_sex in (
        'M', 'F'), f"Student with ID {student_id} has an invalid sex value: {student_sex}"
        assert student_room in rooms_from_db, f"Student with ID {student_id} has an invalid room ID: {student_room}"
        students_from_db[student_id] = {
            'name': student_name,
            'birthday': student_birthday,
            'sex': student_sex,
            'room': student_room
        }
    cursor.close()
    connect_to_db.close()
    assert len(
        students_from_db) == number_of_students, \
        f"Number of students in the database ({len(students_from_db)}) differs from the actual number of students ({number_of_students})"
    for student in students_from_file:
        assert student['id'] in students_from_db, \
            f"Student with ID {student['id']} from JSON file is not found in the database"
        assert students_from_db[student['id']]['name'] == student['name'], \
            f"Student with ID {student['id']} in the database has a different name than in the JSON file"
        assert students_from_db[student['id']]['birthday'] == student['birthday'], \
            f"Student with ID {student['id']} in the database has a different birthday than in the JSON file {student['birthday']}"
        assert students_from_db[student['id']]['sex'] == student['sex'], \
            f"Student with ID {student['id']} in the database has a different sex value than in the JSON file"
        assert students_from_db[student['id']]['room'] == student['room'], \
            f"Student with ID {student['id']} in the database has a different room ID than in the JSON file"