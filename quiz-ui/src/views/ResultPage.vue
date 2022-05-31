<template>
  <h1>Résultat</h1>
  <p>Félicitation {{ playerName }}</p>
  <p>Vous avez obtenu {{ score }} / {{ totalNumberOfQuestion }}</p>
  <h2>Tes voisins de scores</h2>

  <div v-if="playersBefore">...</div>
  <div v-for="scoreEntry in  getFivePlayerNearPlayer()" v-bind:key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>
  <div v-if="playersAfter">...</div>
  <h2>Les 5 meilleurs</h2>
  <div v-for="scoreEntry in  getFiveBest()" v-bind:key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>
  <router-link to="/">Retour à la home</router-link>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "ResultPage",
  data() {
    return {
      registeredScores: [],
      score: 0,
      playerName: '',
      totalNumberOfQuestion: 0,
      playersBefore: false,
      playersAfter: false,
    };
  },
  async created() {
    console.log("Composant Home page 'created'");
    let response = await quizApiService.getQuizInfo();
    this.registeredScores = response.data.scores;
    participationStorageService.saveTotalQuestions(response.data.size);
    this.score = participationStorageService.getParticipationScore();
    this.playerName = participationStorageService.getPlayerName();
    this.totalNumberOfQuestion = participationStorageService.getTotalQuestions();
  },
  methods: {
    getFiveBest() {
      let scores = this.registeredScores;
      scores.sort(function (a, b) {
        return b.score - a.score;
      });
      return scores.slice(0, 5);
    },

    getFivePlayerNearPlayer() {
      let scores = this.registeredScores;
      scores.sort(function (a, b) {
        return b.score - a.score;
      });
      let playerPosition = scores.findIndex(score => score.playerName === this.playerName);
      let fiveBest = scores.slice(playerPosition - 2, playerPosition + 3);
      console.log(playerPosition - 2)
      if (playerPosition - 2 > 1) {
        this.playersBefore = true;
      }
      if (playerPosition + 2 < scores.length - 1) {
        this.playersAfter = true;
      }
      return fiveBest;
    }
  }
};
</script>
