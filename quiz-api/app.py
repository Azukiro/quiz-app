import sqlite3
from flask import Flask, request
from dbServices import DBServices
from jwt_utils import build_token, decode_token
from requestServices import post_question, get_questions, get_question, delete_question, put_question, verifyPosition, post_answers, get_user_infos, post_answers, delete_participants

app = Flask(__name__)


def verify_token(headers):
    auth = headers.get('Authorization')
    if(auth is None):
        return False
    token = auth.split()[1]
    login = decode_token(token)
    if(login != 'quiz-app-admin'):
        return False

    return True


@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():

    nbQuestion, scores = get_user_infos()
    return {'size': nbQuestion, 'scores': scores}, 200


@app.route('/participations', methods=['POST'])
def PostAnswers():

    try:
        good_answers, position_answers, score, playerName = post_answers(
            request.get_json())
    except IndexError as e:
        return {'error': str(e)}, 400
    except sqlite3.IntegrityError as e:
        return str(e), 409
    except Exception as e:
        return str(e), 500

    return {
        'answersSummaries ': {
            'correctAnswerPosition': position_answers,
            'wasCorrect': good_answers
        },
        'playerName': playerName,
        'score': score
    }, 200


@app.route('/participations', methods=['DELETE'])
def DeleteParticipants():

    if(not verify_token(request.headers)):
        return '', 401

    try:
        delete_participants()
    except Exception as e:
        return str(e), 500

    return {}, 204


@app.route('/questions', methods=['GET'])
def GetQuestions():

    questionList = get_questions()
    return str(questionList), 200


@app.route('/questions/<position>', methods=['GET'])
def GetQuestion(position):
    if(not verifyPosition(position)):
        return 'position not found', 404

    try:
        question = get_question(position)
    except Exception as e:
        return str(e), 500

    return question, 200


@app.route('/questions/<position>', methods=['DELETE'])
def DeleteQuestion(position):

    if(not verify_token(request.headers)):
        return '', 401

    if(not verifyPosition(position)):
        return 'Position not found', 404

    try:
        delete_question(position)
    except Exception as e:
        return str(e), 500

    return '', 204


@app.route('/questions/<position>', methods=['PUT'])
def PutQuestion(position):

    if(not verify_token(request.headers)):
        return '', 401

    if(not verifyPosition(position)):
        return 'position not found', 404

    payload = request.get_json()

    try:
        put_question(position, payload)
    except sqlite3.IntegrityError as e:
        return str(e), 409
    except Exception as e:
        return str(e), 500

    return '', 200


@app.route('/questions', methods=['POST'])
def PostQuestion():

    payload = request.get_json()

    if(not verify_token(request.headers)):
        return '', 401

    try:
        post_question(payload)
    except sqlite3.IntegrityError as e:
        return str(e), 409
    except Exception as e:
        return str(e), 500

    return '', 200


@app.route('/login', methods=['POST'])
def Login():
    payload = request.get_json()
    password = payload['password']
    if password == "Vive l'ESIEE !":
        return {'token': build_token()}, 200

    return build_token(), 401


if __name__ == '__main__':
    app.run(ssl_context='adhoc', use_reloader=True, debug=True)
