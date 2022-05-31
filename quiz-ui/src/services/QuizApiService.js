import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true,
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(error);
      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getQuestion(position) {
    return this.call("get", `questions/${position}`);
  },
  postParticipation(participant) {
    return this.call("post", "participations", participant);
  },
  login(credentials) {
    return this.call("post", "login", credentials);
  },
  postQuestion(question, token) {
    return this.call("post", "questions", question, token);
  },
  putQuestion(question, token) {
    return this.call("put", "questions", question, token);
  },
  deleteQuestion(id, token) {
    return this.call("delete", `questions/${id}`, null, token);
  },
};
