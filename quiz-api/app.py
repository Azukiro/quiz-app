from flask import Flask, request
from dbServices import DBServices
from jwt_utils import build_token, decode_token
from requestServices import post_question, get_questions, get_question
app = Flask(__name__)


@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    return {"size": 0, "scores": []}, 200


@app.route('/login', methods=['POST'])
def Login():
    payload = request.get_json()
    password = payload['password']
    if password == "Vive l'ESIEE !":
        return {"token": build_token()}, 200
    return build_token(), 401


if __name__ == "__main__":
    app.run(ssl_context='adhoc', use_reloader=True, debug=True)
