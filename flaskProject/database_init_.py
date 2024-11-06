import psycopg2
from psycopg2 import OperationalError

def create_database_and_table():
    try:
        # Connect to PostgreSQL server
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="nope",
            database="postgres"
        )
        connection.autocommit = True

        # Create a cursor object
        cursor = connection.cursor()

        # Check if the database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'Software_Development_SRH'")
        database_exists = cursor.fetchone()

        if not database_exists:
            # Create a new database
            cursor.execute("CREATE DATABASE Software_Development_SRH")
            print("Database 'Software_Development_SRH' created successfully!")

        # Close the cursor and connection to the default database
        cursor.close()
        connection.close()

    except OperationalError as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    create_database_and_table()
