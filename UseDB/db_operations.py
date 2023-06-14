import os
import mysql.connector
from retry import retry
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

# Database configuration
db_config = {
    "host": os.getenv('MYSQL_HOST'),
    "database": os.getenv('MYSQL_DATABASE'),
    "user": os.getenv('MYSQL_USER'),
    "password": os.getenv('MYSQL_PASSWORD'),
}

# Function to get a user's token from the database
# If the connection to the database fails, it will retry 2 times, and if it still fails, it will return None
@retry(Error, tries=2, delay=2)
def get_token(user_id):
    connection = None
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**db_config)

        cursor = connection.cursor()
        # Use a parameterized query to get the token
        stmt = "SELECT token FROM tokens WHERE user_id = %s"
        cursor.execute(stmt, (user_id,))
        record = cursor.fetchone()
        return record[0] if record else None

    except Error as e:
        print(f"Error reading data from MySQL table: {e}")
        return None

    finally:
        # Disconnect from the database
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


# Function to save a user's token in the database
# If the connection to the database fails, it will retry 2 times
@retry(Error, tries=2, delay=2)
def save_token(user_id, token):
    connection = None
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**db_config)

        cursor = connection.cursor()
        # Use a parameterized query to save the token
        stmt = "INSERT INTO tokens (user_id, token) VALUES (%s, %s)"
        cursor.execute(stmt, (user_id, token))
        connection.commit()

    except Error as e:
        print(f"Error writing data to MySQL table: {e}")

    finally:
        # Disconnect from the database
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Function to delete a user's token from the database
# If the connection to the database fails, it will retry 2 times
@retry(Error, tries=2, delay=2)
def delete_token(user_id):
    connection = None
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**db_config)

        cursor = connection.cursor()
        # Use a parameterized query to delete the token
        stmt = "DELETE FROM tokens WHERE user_id = %s"
        cursor.execute(stmt, (user_id,))
        connection.commit()

    except Error as e:
        print(f"Error deleting data from MySQL table: {e}")

    finally:
        # Disconnect from the database
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@retry(Error, tries=2, delay=2)
def get_model(user_id):
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        stmt = "SELECT model FROM models WHERE user_id = %s"
        cursor.execute(stmt, (user_id,))
        record = cursor.fetchone()
        return record[0] if record else None
    except Error as e:
        print(f"Error reading data from MySQL table: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@retry(Error, tries=2, delay=2)
def save_model(user_id, model):
    connection = None
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**db_config)

        cursor = connection.cursor()
        # Use a parameterized query to save the model
        stmt = "INSERT INTO models (user_id, model) VALUES (%s, %s) ON DUPLICATE KEY UPDATE model = %s"
        cursor.execute(stmt, (user_id, model, model))
        connection.commit()

    except Error as e:
        print(f"Error writing data to MySQL table: {e}")

    finally:
        # Disconnect from the database
        if connection and connection.is_connected():
            cursor.close()
            connection.close()