import sqlite3
from flask import Flask, request
from services import AuthService
from services import RequestServices
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():

    nb_question, scores = RequestServices.get_user_infos()
    return {'size': nb_question, 'scores': scores}, 200


@app.route('/participations', methods=['POST'])
def PostAnswers():

    try:
        good_answers, position_answers, score, player_name = RequestServices.post_answers(
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
        'playerName': player_name,
        'score': score
    }, 200


@app.route('/participations', methods=['DELETE'])
def DeleteParticipants():

    if not AuthService.verify_token(request.headers):
        return '', 401

    try:
        RequestServices.delete_participants()
    except Exception as e:
        return str(e), 500

    return {}, 204


@app.route('/questions', methods=['GET'])
def GetQuestions():

    question_list = RequestServices.get_questions()
    return {"questions": question_list, "size": len(question_list)}, 200


@ app.route('/questions/<position>', methods=['GET'])
def GetQuestion(position):
    if not RequestServices.verifyPosition(position):
        return 'position not found', 404

    try:
        question = RequestServices.get_question(position)
    except Exception as e:
        return str(e), 500

    return question, 200


@ app.route('/questions/<position>', methods=['DELETE'])
def DeleteQuestion(position):

    if not AuthService.verify_token(request.headers):
        return '', 401

    if not RequestServices.verifyPosition(position):
        return 'Position not found', 404

    try:
        RequestServices.delete_question(position)
    except Exception as e:
        return str(e), 500

    return '', 204


@ app.route('/questions/<position>', methods=['PUT'])
def PutQuestion(position):
    if not AuthService.verify_token(request.headers):
        return '', 401

    if not RequestServices.verifyPosition(position):
        return 'position not found', 404

    payload = request.get_json()

    try:
        RequestServices.put_question(position, payload)
    except sqlite3.IntegrityError as e:
        return str(e), 409
    except Exception as e:
        return str(e), 500

    return '', 200


@ app.route('/questions', methods=['POST'])
def PostQuestion():

    payload = request.get_json()

    if not AuthService.verify_token(request.headers):
        return '', 401

    try:
        RequestServices.post_question(payload)
    except sqlite3.IntegrityError as e:
        return str(e), 409
    except Exception as e:
        return str(e), 500

    return '', 200


@ app.route('/login', methods=['POST'])
def Login():
    try:
        token_string = AuthService.login(request.get_json()['password'])
        return {"token": token_string}, 200
    except ValueError as e:
        return str(e), 401


if __name__ == '__main__':

    # use_reloader=True, debug=True
    app.run()
