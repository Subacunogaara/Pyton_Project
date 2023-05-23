import json
import os
import mysql.connector as connection
from db_repository import RoomRepository
import sqlite3
import pytest


password = os.environ.get('PASSWORD_FOR_PYTHON_INTRO')
user = os.environ.get('USER_FOR_PYTHON_INTRO')
host = os.environ.get('HOST_FOR_PYTHON_INTRO')
database_name = os.environ.get('DATABASE_FOR_PYTHON_INTRO')


def test_get_rooms_with_num_students():
    repo = RoomRepository(user=user,
                          password=password,
                          host=host,
                          database=database_name)
    result = json.loads(repo.get_rooms_with_num_students())
    connect_to_db = connection.connect(user=user,
                                       password=password,
                                       host=host,
                                       database=database_name)
    cursor = connect_to_db.cursor()
    sql_query = 'SELECT COUNT(*) - 1 FROM rooms'
    cursor.execute(sql_query)
    number_of_rooms = cursor.fetchone()[0]
    print(number_of_rooms)
    cursor.close()
    connect_to_db.close()

    assert len(result) == number_of_rooms, \
        f"The number of real records {number_of_rooms}, records returned by the function is {len(result)}"
