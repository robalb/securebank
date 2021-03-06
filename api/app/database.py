import mariadb
from fastapi.logger import logger
import os



# configuration used to connect to MariaDB
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
        """
        This is a comment for posterity:
        autocommit disabled has a known issue:
        raising error after a query returned a non-empty set
        causes another error: "Commands out of sync; you can't run this command now"
        This is related to how the context manager handles commits and rollbacks
        https://stackoverflow.com/a/18618363
        This issue interferes with the insufficient_credit exception
        in a couple of transactions.
        The solution is to catch exceptions generated by rollbacks
        """
        #commit logic. Handle rollbacks in case of exceptions
        if not this.autocommit:
            if exc:
                logger.error("ERROR: transaction rollback")
                try:
                  this.conn.rollback()
                except Exception as e:
                  logger.error("ERROR: rollback failed with exception:")
                  logger.error(e)
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


