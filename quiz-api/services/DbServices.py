from models import Question
import sqlite3


class DBServices:

    def __init__(self):
        self.cursor = None
        self.db_connection = None

    def connection(self):
        # création d'un objet connection
        db_connection = sqlite3.connect(
            "./database/db-quizz.db", check_same_thread=False)

        # active stack_trace (slow down the program)
        # db_connection.set_trace_callback(print)
        db_connection.isolation_level = None
        # allow the use of foreign keys
        db_connection.execute("PRAGMA foreign_keys = 1")

        cur = db_connection.cursor()

        self.cursor = cur
        self.db_connection = db_connection

    def close(self):
        self.db_connection.close()

    def dict_factory(self, row):
        '''
        This function is used to convert the result of a query, to a dictionary
        '''
        d = {}
        for idx, col in enumerate(self.cursor.description):
            d[col[0]] = row[idx]
        return d

    def executeSelectQuery(self, query):

        result = self.cursor.execute(query)

        rows = []
        for row in result.fetchall():
            rows.append(self.dict_factory(row))

        return rows

    def executeTransactionQuery(self, query):

        # start transaction
        self.cursor.execute("begin")
        try:
            # save the question to db
            result = self.cursor.execute(query)

            # send the request
            self.cursor.execute("commit")
        except Exception as e:
            # if an error occurs, we rollback the changes
            self.cursor.execute("rollback")
            raise e

        return result.fetchall()
