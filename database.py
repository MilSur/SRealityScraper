import psycopg2

HOST = 'database'
PORT = '5432'
DATABASE = "postgres"
USER = 'postgres'
PASSWORD = 'postgres'

connection = psycopg2.connect(host=HOST, port=PORT, database=DATABASE, user=USER, password=PASSWORD)

def get_db():
    try:
        connection = psycopg2.connect(host=HOST, port=PORT, database=DATABASE, user=USER, password=PASSWORD)
        connection.autocommit = True
        return connection
    except:
        return None
        