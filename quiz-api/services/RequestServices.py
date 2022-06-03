from models import Question
from services.DbServices import DBServices
from datetime import datetime


def get_connection():
    dbConnection = DBServices()
    dbConnection.connection()
    return dbConnection


def verifyPosition(position):
    '''
    Verify if position is valid
    '''

    dbConnection = get_connection()

    result = dbConnection.executeSelectQuery(
        f"SELECT * FROM Question WHERE position={str(position)};")

    dbConnection.close()

    if(len(result) <= 0):
        return False

    return True


def post_question(json_object):
    '''
    Add a new question
    '''

    dbConnection = get_connection()

    question = Question.deserialize(json_object)

    dbConnection.executeTransactionQuery(
        f"UPDATE Question SET position = position + 1 WHERE position >= {str(question.position)};")

    questionRequest = f"INSERT INTO question (title, text, image, position) VALUES (\"{question.title}\", \"{question.text}\", \"{question.image }\", {str(question.position)});"
    dbConnection.executeTransactionQuery(questionRequest)

    result = dbConnection.executeSelectQuery(
        "SELECT seq FROM sqlite_sequence WHERE name='Question';")

    if(len(result) != 1):
        raise Exception("Error while inserting question")

    question.id = result[0]["seq"]

    for answer in question.answers:
        answerRequest = f"INSERT INTO answer (text, isCorrect, question_id) VALUES (\"{answer.text }\", {str(answer.correct)}, {str(question.id)});"
        dbConnection.executeTransactionQuery(answerRequest)

    dbConnection.close()


def get_questions():
    '''
    Get all questions
    '''

    dbConnection = get_connection()

    result = dbConnection.executeSelectQuery(
        "SELECT * FROM Question ORDER BY position;")

    if(len(result) <= 0):
        raise Exception("No questions found")

    for obj in result:
        answers = dbConnection.executeSelectQuery(
            f"SELECT text, isCorrect FROM Answer WHERE Answer.question_id = \"{str(obj['id'])}\";")

        obj["possibleAnswers"] = answers

        for answer in obj["possibleAnswers"]:
            answer["isCorrect"] = bool(answer["isCorrect"])

    dbConnection.close()

    return result


def get_question(position):
    '''
    Get a question by position
    '''

    dbConnection = get_connection()

    result = dbConnection.executeSelectQuery(
        f"SELECT * FROM Question WHERE position={position};")

    if(len(result) != 1):
        raise Exception("No questions found")

    question = result[0]
    answers = dbConnection.executeSelectQuery(
        f"SELECT text, isCorrect FROM Answer WHERE Answer.question_id = {str(question['id'])};")

    dbConnection.close()

    question["possibleAnswers"] = answers
    for answer in question["possibleAnswers"]:
        answer["isCorrect"] = bool(answer["isCorrect"])

    return question


def delete_question(position):
    '''
    Delete a question
    '''

    dbConnection = get_connection()

    dbConnection.executeTransactionQuery(
        f"DELETE FROM Question WHERE position={str(position)};")

    dbConnection.executeTransactionQuery(
        f"UPDATE Question SET position = position - 1 WHERE position >= {str(position)};")

    dbConnection.close()


def put_question(position, json_obj):
    '''
    Update a question with the new values and move is position if needed
    '''

    question = Question.deserialize(json_obj)
    dbConnection = get_connection()
    position = int(position)

    result = dbConnection.executeSelectQuery(
        f"SELECT id FROM Question WHERE position={str(position)};")

    if(len(result) != 1):
        raise Exception("No questions found")

    id = result[0]['id']

    # update position of other question
    if(position != question.position):

        sign = 1 if question.position > position else -1

        while(position != question.position):
            dbConnection.executeTransactionQuery(
                f"UPDATE Question SET position=position + {str(-sign)} WHERE position={str(position+sign)};")

            position += sign

    # update question where position = position
    dbConnection.executeTransactionQuery(
        f"UPDATE Question SET title= \"{question.title}\", text= \"{question.text}\", image= \"{question.image}\", position={str(question.position)} WHERE id={str(id)};")

    # update answers by delete and insert
    dbConnection.executeTransactionQuery(
        f"DELETE FROM Answer WHERE question_id={str(id)};")

    for answer in question.answers:
        dbConnection.executeTransactionQuery(
            f"INSERT INTO Answer (question_id, text, isCorrect) VALUES ({str(id)}, \"{answer.text}\", {str(answer.correct)});")

    dbConnection.close()


def get_user_infos():
    '''
    Get all user infos
    '''

    dbConnection = get_connection()

    result = dbConnection.executeSelectQuery(
        "SELECT COUNT(*) as nbQuestion FROM Question;")

    if(len(result) <= 0):
        raise Exception("No questions found")

    nbQuestion = result[0]['nbQuestion']

    # get participants info
    result = dbConnection.executeSelectQuery(
        "SELECT * FROM Participant ORDER BY score DESC;")

    dbConnection.close()

    return nbQuestion, result


def post_answers(json_object):
    '''
    Save to the database the answers of the user and create the user
    '''

    playerName = json_object['playerName']
    answers = json_object['answers']

    dbConnection = get_connection()

    result = dbConnection.executeSelectQuery(
        "SELECT id FROM Question ORDER BY position;")

    if(len(result) <= 0):
        raise Exception("No questions found")

    elif(len(result) != len(answers)):
        raise IndexError(
            "Number of answers is not the same as number of questions")

    position_answers = []
    good_answers = []
    for(i, obj) in enumerate(result):
        id = obj['id']
        # select answer
        resultAnswer = dbConnection.executeSelectQuery(
            f"SELECT * FROM Answer WHERE question_id={str(id)};")

        if(len(resultAnswer) <= 0):
            raise Exception("No answers found")

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

    dbConnection.executeTransactionQuery(
        f"INSERT INTO Participant (playerName, score, date) VALUES (\"{playerName}\", {str(score)}, \"{dt_string}\");")

    dbConnection.close()

    return good_answers, position_answers, score, playerName


def delete_participants():
    '''
    Delete all participants
    '''

    dbConnection = get_connection()

    dbConnection.executeTransactionQuery("DELETE FROM Participant;")

    dbConnection.close()
