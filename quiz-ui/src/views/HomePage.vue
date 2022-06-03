<template>
  <div class="container-sm text-center w-25 mt-5">
    <h1 class="text-uppercase display-4">Meilleurs scores</h1>

    <div class="table-wrapper-scroll-y my-custom-scrollbar rounded border border-light mt-5 mb-5">
      <table class="table table-striped table-dark table-bordered table-hover">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Pseudo</th>
            <th scope="col">Score</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(scoreEntry, index) in registeredScores" :key="scoreEntry.date">
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ scoreEntry.playerName }}</td>
            <td>{{ scoreEntry.score }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <button class="btn btn-primary btn-lg" type="button" @click="$router.push('start-new-quiz-page')">Démarrer le
      quiz!</button>
    <!-- <router-link to="/start-new-quiz-page">Démarrer le quiz !</router-link> -->
  </div>
</template>

<script>

import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: [],
    };
  },

  async created() {

    let response = await quizApiService.getQuizInfo();
    this.registeredScores = response.data.scores;
    participationStorageService.saveTotalQuestions(response.data.size);

  }
};
</script>
