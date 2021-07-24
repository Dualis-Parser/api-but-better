import mysql.connector
from mysql.connector.cursor import MySQLCursorPrepared

from os import environ


class MySQL:
    def __init__(self):
        return
        self.cnx = mysql.connector.connect(user=environ.get("DATABASE_USER"), password=environ.get("DATABASE_PASSWORD"),
                                           host=environ.get("DATABASE_HOST"), database=environ.get("DATABASE_NAME"),
                                           use_pure=True)

    def query(self, query, params):
        return []
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
        return
        self.cnx.close()
