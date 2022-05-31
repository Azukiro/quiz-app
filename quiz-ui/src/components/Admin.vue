<script setup>

</script>

<template>
  <header>
    <h1> Admin </h1>

    <div v-if="!adminMode" class="wrapper">
      <input type="password" v-model="password" placeholder="mot de passe">
      <button type="button" @click="checkPassword">Valider</button>
      <p v-if="errorLogin"> Erreur d'identifiant </p>
    </div>
    <div v-if="adminMode" class="wrapper">
      <QuestionEdition />
      <button type="button" @click="logout">Logout</button>
    </div>
  </header>
</template>


<script>
import quizApiService from "@/services/QuizApiService";
import adminStorageService from "@/services/AdminStorageService";
import QuestionEdition from '@/components/QuestionEdition.vue'
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