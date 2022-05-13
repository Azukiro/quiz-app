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
        answers = dbService.executeSelectQuery(
            "SELECT * FROM Answer WHERE Answer.question_id = \""+str(obj['id'])+"\";")

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

    question = result[0]
    answers = dbService.executeSelectQuery(
        "SELECT * FROM Answer WHERE Answer.question_id = "+str(question['id'])+";")

    print(answers)
    question["possibleAnswers"] = answers
    for answer in question["possibleAnswers"]:
        answer["isCorrect"] = bool(answer["isCorrect"])
    dbService.close()

    return question


def delete_question(position):
    dbService = DBServices()
    dbService.connection()

    dbService.executeTransactionQuery(
        "DELETE FROM Question WHERE position = " + position)
    dbService.close()


# def put_question(position):
#     dbService = DBServices()
#     dbService.connection()

#     dbService.executeTransactionQuery(
#         "DELETE FROM Question WHERE position = " + position)
#     dbService.close()
