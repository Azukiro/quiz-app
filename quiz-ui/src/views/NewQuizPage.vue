<template>
  <div class="new-quiz">
    <h1>This is an new quiz page</h1>
    <form>
      <p>Saisissez votre nom</p>
      <input type="text" v-model="username" placeholder="UserName">
      <p>{{ username }}</p>
      <button type="button" @click="launchNewQuiz">Start Quiz</button>
    </form>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .new-quiz {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>

<script>
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "NewQuizPage",

  data() {
    return {
      username: '',
    };
  },
  methods: {

    launchNewQuiz() {
      console.log("Launch new quiz with", this.username);
      participationStorageService.savePlayerName(this.username);
      this.$router.push('/questions');
    },

  }
};
</script>
