from flask import Flask, request
from dbServices import DBServices
from jwt_utils import build_token, decode_token
from requestServices import post_question, get_questions, get_question, delete_question, put_question

app = Flask(__name__)


def verify_token(headers):
    auth = headers.get('Authorization')
    if(auth is None):
        return False
    token = auth.split()[1]
    login = decode_token(token)
    if(login != "quiz-app-admin"):
        return False

    return True


@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():

    return {"size": 0, "scores": []}, 200


@app.route('/questions', methods=['GET'])
def GetQuestions():

    questionList = get_questions()
    return str(questionList), 200


@app.route('/questions/<position>', methods=['GET'])
def GetQuestion(position):

    question = get_question(position)
    return question, 200


@app.route('/questions/<position>', methods=['DELETE'])
def DeleteQuestion(position):

    if(not verify_token(request.headers)):
        return "", 401
    delete_question(position)
    return '', 204


@app.route('/questions/<position>', methods=['PUT'])
def PuteQuestion(position):

    if(not verify_token(request.headers)):
        return "", 401
    payload = request.get_json()
    put_question(position, payload)
    return '', 200


@app.route('/questions', methods=['POST'])
def PostQuestion():

    payload = request.get_json()

    if(not verify_token(request.headers)):
        return "", 401

    try:

        post_question(payload)
    except:
        return '', 500

    return "", 200


@app.route('/login', methods=['POST'])
def Login():
    payload = request.get_json()
    password = payload['password']
    if password == "Vive l'ESIEE !":
        return {"token": build_token()}, 200
    return build_token(), 401


if __name__ == "__main__":
    app.run(ssl_context='adhoc', use_reloader=True, debug=True)
