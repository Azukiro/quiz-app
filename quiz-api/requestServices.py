from models import Question, Answer
from dbServices import DBServices


def post_question(json_object):

    dbService = DBServices()
    dbService.connection()

    question = Question.deserialize(json_object)
    dbService.insertQuestion(question)

    dbService.close()


def get_questions():

    dbService = DBServices()
    dbService.connection()

    result = dbService.executeSelectQuery("SELECT * FROM Question;")
    if(len(result) <= 0):
        Exception("No questions found")

    questionList = []
    for obj in result:
        print("SELECT * FROM Answer WHERE Answer.question_fk = " +
              obj['title']+";")
        answers = dbService.executeSelectQuery(
            "SELECT * FROM Answer WHERE Answer.question_fk = \""+obj['title']+"\";")

        obj["possibleAnswers"] = answers

        # questionList.append(Question.deserialize(obj))

    dbService.close()
    print(result)
    return result


def get_question(position):
    dbService = DBServices()
    dbService.connection()

    result = dbService.executeSelectQuery(
        "SELECT * FROM Question WHERE position = " + position)

    if(len(result) != 1):
        Exception("No questions found")

    dbService.close()
