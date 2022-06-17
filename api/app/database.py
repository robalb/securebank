import mariadb
from fastapi.logger import logger
import os



# configuration used to connect to MariaDB and sqlalchemy
config = {
    'host': os.environ['MARIADB_HOST'],
    'port': 3306,
    'user': os.environ['MARIADB_USER'],
    'password': os.environ['MARIADB_PASSWORD'],
    'database': os.environ['MARIADB_DATABASE']
}

def get_conn():
    return mariadb.connect(**config)


class Cursor:
    def __init__(this, autocommit=True):
        this.autocommit = autocommit

    def __enter__(this):
        this.conn = get_conn()
        if this.autocommit:
            this.conn.autocommit = True
        this.cur = this.conn.cursor(dictionary=True)
        return this.cur

    def __exit__(this, exc, value, tb):
        #commit logic. Handle rollbacks in case of exceptions
        if not this.autocommit:
            if exc:
                logger.error("ERROR: transaction rollback")
                this.conn.rollback()
            else:
                this.conn.commit()
        this.cur.close()
        this.conn.close()


class Pool:
    """ TODO: work on this, replace get_conn"""

    def __init__(this):
        this.pool = None
        this.create_connection_pool()

    def create_connection_pool(this):
        """Attempts to create a connection pool"""
        try:
            this.pool = mariadb.ConnectionPool(
                    host= os.environ['MARIADB_HOST'],
                    port= 3306,
                    user= os.environ['MARIADB_USER'],
                    password= os.environ['MARIADB_PASSWORD'],
                    database= os.environ['MARIADB_DATABASE'],
                    pool_name='web-app',
                    pool_size=5)
        except:
            logger.error("ERROR: could not create connection pool")

    def get_connection(this, attempt=0):
        """Returns a connection from the pool
           If the pool is empty it will try to create a new one.
           It will make 5 attempts, then an error will be thrown
        """
        if this.pool is not None:
            return this.pool.get_connection()
        elif attempt < 5:
            logger.error(f"ERROR: no pool. Attempt {attempt}")
            # attempts to create the pool
            this.create_connection_pool()
            return this.get_connection(attempt + 1)


