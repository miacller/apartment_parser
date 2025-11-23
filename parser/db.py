#parser/db.py
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def sql_connection():
    config = {
        'user': os.getenv("DB_USER"), 
        'password': os.getenv("DB_PASSWORD"),
        'host': os.getenv("DB_HOST"),
        'database': os.getenv("DB_NAME")
    }
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS apartments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            deal_id VARCHAR(200),
            price VARCHAR(200),
            area VARCHAR(200),
            addres VARCHAR(200),
            rooms VARCHAR(200),
            house_type VARCHAR(200),
            decoration VARCHAR(200),
            number_of_lifts VARCHAR(200),
            floor VARCHAR(200),
            number_of_floors VARCHAR(200)
        )
        """)
        connection.commit()
        return connection
    
    except mysql.connector.Error as err:
        return None
