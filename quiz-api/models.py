# Exemple de création de classe en python
class Question():
    def init(self, title: str, text: str, image: str, position: int, answers: list):
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.answers = answers

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
        print(json_object)
        question = Question()
        question.title = json_object['title']
        question.text = json_object['text']
        question.image = json_object['image']
        question.position = json_object['position']
        answers_list = []
        for obj in json_object["possibleAnswers"]:
            answers_list.append(Answer.deserialize(obj))

        question.answers = answers_list
        return question


class Answer():
    def init(self, text: str, correct: bool):
        self.text = text
        self.correct = correct

    def serialize(self):
        return {
            'text': self.text,
            'isCorrect': self.correct
        }

    @staticmethod
    def deserialize(json_object):

        answer = Answer()
        answer.text = json_object['text']
        answer.correct = json_object['isCorrect']

        return answer
