<script setup>
import QuestionList from "./QuestionList.vue";

</script>

<template>
  <div class="container-sm text-center w-25 mt-5">
    <h2> Connexion </h2>

    <div v-if="!adminMode" class="wrapper">
      <input type="password" v-model="password" placeholder="mot de passe">
      <br>
      <button class="btn btn-success mt-3" type="button" @click="checkPassword">Connexion</button>
      <p v-if="errorLogin"> Erreur d'identifiant </p>
    </div>
    <div v-if="adminMode" class="wrapper">
      <QuestionList />
      <br>
      <button class="btn btn-primary mt-3" type="button" @click="logout">Logout</button>
    </div>
  </div>
</template>


<script>
import quizApiService from "@/services/QuizApiService";
import adminStorageService from "@/services/AdminStorageService";
export default {
  data() {
    return {
      errorLogin: false,
      password: '',
      adminMode: false,
    }
  },
  methods: {
    async checkPassword() {
      console.log("tototo")
      let response = await quizApiService.login({ password: this.password });
      if (response && response.status === 200) {
        this.errorLogin = false;
        this.adminMode = true;
        console.log("titi")
        //save token
        adminStorageService.saveToken(response.data.token);
      } else {
        this.errorLogin = true;
      }
    },

    logout() {
      adminStorageService.clear();
      this.adminMode = false;
    }
  },
}

</script>