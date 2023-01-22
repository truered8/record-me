import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"), connect_args={'sslmode': 'verify-ca'})
connection = engine.connect()
# print(connection.execute(text("INSERT INTO groups VALUES ('df9d7ca8-f71f-4b1c-94aa-d5159e2e73ac', 'Group 1')")).fetchall())
print(connection.execute(text("SELECT * FROM groups")).fetchall())
