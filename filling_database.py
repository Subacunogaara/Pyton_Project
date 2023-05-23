import json
import mysql.connector as connection
import os
import logging


# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('logfile.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info('Script is started')

# Open JSON files with data
with open ('students.json', 'r') as file_1, open ('rooms.json', 'r') as file_2:
    students = json.load(file_1)
    rooms = json.load(file_2)

# Make a connection to database and cursor
password = os.environ.get('PASSWORD_FOR_PYTHON_INTRO')
user = os.environ.get('USER_FOR_PYTHON_INTRO')
host = os.environ.get('HOST_FOR_PYTHON_INTRO')
database_name = os.environ.get('DATABASE_FOR_PYTHON_INTRO')
con_to_db = connection.connect(user=user,
                               password=password,
                               host=host,
                               database=database_name)
cursor = con_to_db.cursor()

# Filling the rooms table
for room in rooms:
    sql_query_rooms = 'INSERT INTO rooms (id, name) VALUES (%s, %s)'
    values_for_fill_rooms = (room['id'],
                             room['name'])
    cursor.execute(sql_query_rooms, values_for_fill_rooms)

# Filling the students table
for student in students:
    sql_query_students = 'INSERT INTO students (id, name, birthday, sex, room) VALUES (%s, %s, %s, %s, %s)'
    values_for_fill_students = (student['id'],
                                student['name'],
                                student['birthday'],
                                student['sex'],
                                student['room'])
    cursor.execute(sql_query_students, values_for_fill_students)

# Commit and closing connections
con_to_db.commit()
cursor.close()
con_to_db.close()

logger.info('Script is finished')
