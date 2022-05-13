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
        db_connection.set_trace_callback(print)
        db_connection.isolation_level = None

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

        try:
            # save the question to db
            result = self.cursor.execute(query)

            # send the request
            self.cursor.execute("commit")
        except Exception:
            self.cursor.execute("rollback")

        return result.fetchall()

    def insertQuestion(self, question: Question):

        questionRequest = "INSERT INTO question (title, text, image, position) VALUES (\"" + question.title + \
            "\", \"" + question.text + "\", \"" + question.image + \
            "\", " + str(question.position) + ")"
        self.executeTransactionQuery(questionRequest)

        for answer in question.answers:
            answerRequest = "INSERT INTO answer (text, isCorrect, question_fk) VALUES (\"" + \
                answer.text + "\", " + str(answer.correct) + \
                ", \"" + question.title + "\")"
            self.executeTransactionQuery(answerRequest)
