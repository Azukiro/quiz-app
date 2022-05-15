from models import Question, Answer
import sqlite3


class DBServices:

    def __init__(self):
        self.cursor = None
        self.db_connection = None

    def connection(self):
        # création d'un objet connection
        db_connection = sqlite3.connect(
            "./db-quizz.db", check_same_thread=False)
        # set the sqlite connection in "manual transaction mode"
        # (by default, all execute calls are performed in their own transactions, not what we want)
        # db_connection.set_trace_callback(print)
        db_connection.isolation_level = None
        db_connection.execute("PRAGMA foreign_keys = 1")

        cur = db_connection.cursor()

        self.cursor = cur
        self.db_connection = db_connection

    def close(self):
        self.db_connection.close()

    def dict_factory(self, row):
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

        # save the question to db
        result = self.cursor.execute(query)

        # send the request
        self.cursor.execute("commit")

        return result.fetchall()

    def insertQuestion(self, question: Question):

        questionRequest = "INSERT INTO question (title, text, image, position) VALUES (\"" + question.title + \
            "\", \"" + question.text + "\", \"" + question.image + \
            "\", " + str(question.position) + ")"
        self.executeTransactionQuery(questionRequest)

        result = self.executeSelectQuery(
            "select seq from sqlite_sequence where name='Question'")

        if(len(result) != 1):
            Exception("Mauvaise création de question")

        question.id = result[0]["seq"]

        for answer in question.answers:
            answerRequest = "INSERT INTO answer (text, isCorrect, question_id) VALUES (\"" + \
                answer.text + "\", " + str(answer.correct) + \
                ", " + str(question.id) + ")"
            self.executeTransactionQuery(answerRequest)
