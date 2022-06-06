<template>
  <div class="container-sm text-center w-25 mt-5 mb-5">
    <h1 class="text-uppercase display-4">
      Démarrage du DeweyQuiz
    </h1>
    <form>
      <p>Saisissez votre nom</p>
      <input type="text" v-model="username" placeholder="UserName">
      <br>
      <button class="btn btn-primary btn-lg mt-3" type="button" @click="launchNewQuiz">Start Quiz</button>
    </form>
  </div>
</template>

<style>
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
