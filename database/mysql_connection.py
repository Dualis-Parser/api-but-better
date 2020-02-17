import mysql.connector
from mysql.connector import errorcode
from mysql.connector.cursor import MySQLCursorPrepared

from os import environ

class MySQL:
    def __init__(self):
        try:
            self.cnx = mysql.connector.connect(user=environ.get("DATABASE_USER"), password=environ.get("DATABASE_PASSWORD"),
                                               host=environ.get("DATABASE_HOST"), database=environ.get("DATABASE_NAME"),
                                               use_pure=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def query(self, query, params):
        cursor = self.cnx.cursor(cursor_class=MySQLCursorPrepared)
        cursor.execute(query, params)

        result = []
        try:
            result = cursor.fetchall()
        except mysql.connector.errors.InterfaceError:
            # no result
            pass

        cursor.close()
        # commit in case of changes
        self.cnx.commit()

        return result

    def close(self):
        self.cnx.close()
