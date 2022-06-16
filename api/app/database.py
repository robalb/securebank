# Module Import
import mariadb
import os

config = {
    'host': os.environ['MARIADB_HOST'],
    'port': 3306,
    'user': os.environ['MARIADB_USER'],
    'password': os.environ['MARIADB_PASSWORD'],
    'database': os.environ['MARIADB_DATABASE']
}

def create_connection_pool():
    """Creates and returns a Connection Pool"""

    # Create Connection Pool
    pool = mariadb.ConnectionPool(
            host= os.environ['MARIADB_HOST'],
            port= 3306,
            user= os.environ['MARIADB_USER'],
            password= os.environ['MARIADB_PASSWORD'],
            database= os.environ['MARIADB_DATABASE'],
            pool_name='web-app',
            pool_size=5)

    # Return Connection Pool
    return pool


