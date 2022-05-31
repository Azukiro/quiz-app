<template>
  <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
  <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />
</template>

<script>
import QuestionDisplay from './QuestionDisplay.vue'
import participationStorageService from '@/services/ParticipationStorageService';
import quizApiService from '@/services/QuizApiService';
export default {
  data() {
    return {
      currentQuestionPosition: 1,
      totalNumberOfQuestion: 0,
      currentQuestion: {},
      selectedAnswer: [],
    }
  },
  components: {
    QuestionDisplay
  },
  methods: {
    async loadQuestionByPosition() {
      let response = await quizApiService.getQuestion(this.currentQuestionPosition);
      this.currentQuestion = response.data;
    },

    async answerClickedHandler(index) {
      console.log("Composant QuestionDisplay 'answerClickedHandler'");
      this.selectedAnswer.push(index);
      if (this.currentQuestionPosition >= this.totalNumberOfQuestion) {
        this.endQuiz();
      } else {
        this.currentQuestionPosition++;
        this.loadQuestionByPosition();
      }
    },

    async endQuiz() {
      console.log("Composant QuestionDisplay 'endQuiz'");
      let participant = {
        playerName: participationStorageService.getPlayerName(),
        answers: this.selectedAnswer,
      }
      let response = await quizApiService.postParticipation(participant);
      participationStorageService.saveParticipationScore(response.data.score);
      this.$router.push('/result');
    },
  },


  async created() {
    console.log("Composant QuestionDisplay 'created'");
    this.totalNumberOfQuestion = participationStorageService.getTotalQuestions();
    this.loadQuestionByPosition();
  },




}
</script>