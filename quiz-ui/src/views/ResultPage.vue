<template>
  <div class="container text-center mt-5">
    <h1>Résultat</h1>
    <p>Félicitation {{ playerName }}</p>
    <p>Vous avez obtenu {{ score }} / {{ totalNumberOfQuestion }}</p>
    <div class="container">
      <div class="row">
        <div class="col-sm">
          <h2>Tes voisins de scores</h2>

          <div class="rounded border border-light mt-5 mb-5">
            <table class="table table-striped table-dark table-bordered table-hover">
              <thead>
                <tr>
                  <th scope="col">Pseudo</th>
                  <th scope="col">Score</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="playersBefore">
                  <td>...</td>
                  <td>...</td>
                </tr>
                <tr v-for="(scoreEntry, index) in getFivePlayerNearPlayer()" :key="scoreEntry.date">
                  <td>{{ scoreEntry.playerName }}</td>
                  <td>{{ scoreEntry.score }}</td>
                </tr>
                <tr v-if="playersAfter">
                  <td>...</td>
                  <td>...</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="col-sm">
          <h2>Les 5 meilleurs</h2>
          <div class="rounded border border-light mt-5 mb-5">
            <table class="table table-striped table-dark table-bordered table-hover">
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">Pseudo</th>
                  <th scope="col">Score</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(scoreEntry, index) in getFiveBest()" :key="scoreEntry.date">
                  <th scope="row">{{ index + 1 }}</th>
                  <td>{{ scoreEntry.playerName }}</td>
                  <td>{{ scoreEntry.score }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <button class="btn btn-primary btn-lg" type="button" @click="$router.push('/')">Retour à la home</button>
  </div>
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

    let response = await quizApiService.getQuizInfo();
    participationStorageService.saveTotalQuestions(response.data.size);

    this.registeredScores = response.data.scores;
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
