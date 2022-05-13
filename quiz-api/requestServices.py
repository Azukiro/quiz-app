from models import Question, Answer
from dbServices import DBServices


def post_question(json_object):

    dbService = DBServices()
    dbService.connection()

    question = Question.deserialize(json_object)

    dbService.executeTransactionQuery(
        "UPDATE Question SET position = position + 1 WHERE position >= "+str(question.position))

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
    dbService.executeTransactionQuery(
        "UPDATE Question SET position = position - 1 WHERE position >= "+str(position))

    dbService.close()


def put_question(position, json_obj):

    question = Question.deserialize(json_obj)
    dbService = DBServices()
    dbService.connection()
    position = int(position)

    result = dbService.executeSelectQuery(
        "SELECT id FROM Question WHERE position = " + str(position))
    print(len(result))
    if(len(result) != 1):
        Exception("No questions found")

    id = result[0]['id']

    if(position != question.position):

        sign = 1 if question.position > position else -1

        print(str(sign))
        while(position != question.position):

            # dbService.executeTransactionQuery(
            #     "UPDATE Question SET position = position + " + str(sign) + " WHERE position = " + str(position))
            # break
            dbService.executeTransactionQuery(
                "UPDATE Question SET position = position + " + str(-sign) + " WHERE position = " + str(position+sign))

            position += sign

    # update question where position = position
    dbService.executeTransactionQuery(
        "UPDATE Question SET title = \""+question.title+"\", text = \""+question.text+"\", image = \""+question.image+"\", position="+str(question.position)+" WHERE id = "+str(id))

    dbService.close()
