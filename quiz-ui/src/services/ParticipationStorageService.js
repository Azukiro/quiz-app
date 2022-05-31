export default {
  clear() {
    // todo : implement
  },
  savePlayerName(playerName) {
    window.localStorage.setItem("playerName", playerName);
  },
  getPlayerName() {
    return window.localStorage.getItem("playerName");
  },
  saveParticipationScore(participationScore) {
    window.localStorage.setItem("participationScore", participationScore);
  },
  getParticipationScore() {
    return window.localStorage.getItem("participationScore");
  },
  incrementParticipationScore() {
    let participationScore = this.getParticipationScore();
    participationScore++;
    this.saveParticipationScore(participationScore);
  },

  saveTotalQuestions(total) {
    window.localStorage.setItem("totalQuestions", total);
  },
  getTotalQuestions() {
    return window.localStorage.getItem("totalQuestions");
  },
};
