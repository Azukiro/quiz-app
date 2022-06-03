<script setup>
import QuestionList from "./QuestionList.vue";

</script>

<template>
  <h1> Admin </h1>

  <div v-if="!adminMode" class="wrapper">
    <input type="password" v-model="password" placeholder="mot de passe">
    <button class="btn btn-primary" type="button" @click="checkPassword">Valider</button>
    <p v-if="errorLogin"> Erreur d'identifiant </p>
  </div>
  <div v-if="adminMode" class="wrapper">
    <QuestionList />
    <br>
    <button class="btn btn-primary mt-3" type="button" @click="logout">Logout</button>
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