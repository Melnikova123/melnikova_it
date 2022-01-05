import psycopg2

from utils.config import DATABASE_URL

conn = psycopg2.connect(database='postgres',
                        user='postgres',
                        password='root',
                        host="localhost",
                        port="5432")
cur = conn.cursor()
