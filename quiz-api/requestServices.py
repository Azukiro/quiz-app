from models import Question, Answer
from dbServices import DBServices
from datetime import datetime


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
        "DELETE FROM Question WHERE position = " + str(position))

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

    # update answers by delete and insert
    dbService.executeTransactionQuery(
        "DELETE FROM Answer WHERE question_id = "+str(id))

    for answer in question.answers:
        dbService.executeTransactionQuery(
            "INSERT INTO Answer (question_id, text, isCorrect) VALUES ("+str(id)+", \""+answer.text+"\", "+str(answer.correct)+");")

    dbService.close()


def verifyPosition(position):
    dbService = DBServices()
    dbService.connection()

    print("toto")
    print("SELECT * FROM Question WHERE position = " + str(position))

    result = dbService.executeSelectQuery(
        "SELECT * FROM Question WHERE position = " + str(position))

    dbService.close()
    if(len(result) <= 0):
        return False

    return True


def get_user_infos():
    # get Nb Question
    dbService = DBServices()
    dbService.connection()

    result = dbService.executeSelectQuery(
        "SELECT COUNT(*) as nbQuestion FROM Question;")
    if(len(result) <= 0):
        Exception("No questions found")

    nbQuestion = result[0]['nbQuestion']

    # get participants info
    result = dbService.executeSelectQuery(
        "SELECT * FROM Participant;")

    return nbQuestion, result


def post_answers(playload):

    playerName = playload['playerName']
    answers = playload['answers']

    dbService = DBServices()
    dbService.connection()

    # get all question and answers from db
    result = dbService.executeSelectQuery(
        "SELECT id FROM Question ORDER BY position;")

    if(len(result) <= 0):
        Exception("No questions found")

    position_answers = []
    good_answers = []
    for(i, obj) in enumerate(result):
        id = obj['id']
        # select answer
        resultAnswer = dbService.executeSelectQuery(
            "SELECT * FROM Answer WHERE question_id = " + str(id))

        if(len(resultAnswer) <= 0):
            Exception("No answers found")

        for(j, answer) in enumerate(resultAnswer):
            if(answer['isCorrect'] == 1):
                position_answers.append(j+1)
                if(j+1 == answers[i]):
                    good_answers.append(True)
                else:
                    good_answers.append(False)
                break

    # count goodAnswers with lambda
    score = len(list(filter(lambda x: x, good_answers)))
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    dbService.executeTransactionQuery(
        "INSERT INTO Participant (playerName, score, date) VALUES (\""+playerName+"\", "+str(score)+", \""+dt_string+"\");")

    return good_answers, position_answers, score, playerName
