import json
import psycopg2

DATABASE = 'flask_db'
TABLE = 'items'
USER = 'flask_db_user'
PASSWORD = 'flask_db_password'
HOST = 'localhost'


def connect_to_db():
    """function to create a connection to db"""
    connection = psycopg2.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD
    )
    # We call the table creation function when the conn is established
    create_table(connection)
    return connection


def create_table(connection):
    """Function to create a table in database"""
    cursor = connection.cursor()
    # if table isn't exist, we create a new one
    cursor.execute(f'CREATE TABLE IF NOT EXISTS items ('
                   f'id serial NOT NULL PRIMARY KEY, '
                   f'info json NOT NULL)')
    connection.commit()
    cursor.close()


def save_to_db(items):
    """Saves data to database"""
    connection = connect_to_db()
    cursor = connection.cursor()
    # making query
    insert_query = """INSERT INTO items (info) VALUES (%s);"""
    # whe iterate over the getting data
    for item in items:
        # print data in terminal
        print(item)
        # creating json type data
        record = json.dumps(item)
        # and insert data in db using insert query
        cursor.execute(insert_query, [record])
    connection.commit()
    cursor.close()
    connection.close()
