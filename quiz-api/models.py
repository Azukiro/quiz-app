# Exemple de création de classe en python
class Question():
    def __init__(self, title: str, text: str, image: str, position: int):
        self.id = -1
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.answers = []

    def serialize(self):
        return {
            'title': self.title,
            'text': self.text,
            'image': self.image,
            'position': self.position,
            'answers': [answer.serialize() for answer in self.answers]
        }

    @staticmethod
    def deserialize(json_object):
        question = Question(
            json_object['title'], json_object['text'], json_object['image'], json_object['position'])
        answers_list = []
        for obj in json_object["possibleAnswers"]:
            answers_list.append(Answer.deserialize(obj))

        question.answers = answers_list
        return question


class Answer():
    def __init__(self, text: str, correct: bool):
        self.text = text
        self.correct = correct

    def serialize(self):
        return {
            'text': self.text,
            'isCorrect': self.correct
        }

    @staticmethod
    def deserialize(json_object):

        answer = Answer(json_object['text'], json_object['isCorrect'])
        return answer
