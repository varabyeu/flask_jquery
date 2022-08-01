import json
import psycopg2

DATABASE = 'flask_db'
TABLE = 'items'
USER = 'flask_db_user'
PASSWORD = 'flask_db_password'
HOST = 'localhost'


def connect_to_db():
    connection = psycopg2.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD
    )
    create_table(connection)
    return connection


def create_table(connection):
    cursor = connection.cursor()
    cursor.execute(f'CREATE TABLE IF NOT EXISTS items ('
                   f'id serial NOT NULL PRIMARY KEY, '
                   f'info json NOT NULL)')
    table_created = True
    connection.commit()
    cursor.close()
    return table_created


def save_to_db(items):
    connection = connect_to_db()
    cursor = connection.cursor()
    insert_query = """INSERT INTO items (info) VALUES (%s);"""
    for item in items:
        print(item)
        record = json.dumps(item)
        cursor.execute(insert_query, [record])
    connection.commit()
    cursor.close()
    connection.close()
