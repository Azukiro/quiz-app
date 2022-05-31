

<template>
  <header>
    <h1> Admin </h1>

    <div v-if="!adminMode" class="wrapper">
      <input type="password" v-model="password" placeholder="mot de passe">
      <button type="button">Valider</button>
      <p v-if="errorLogin"> Erreur d'identifiant </p>
    </div>
    <div v-if="adminMode" class="wrapper">
      <button type="button" @click="logout">Logout</button>
    </div>
  </header>
</template>


<script>
import quizApiService from "@/services/QuizApiService";
export default {
  data() {
    return {
      errorLogin: false,
      password: '',
      adminMode: false,
    }
  },
  methods: {
    checkPassword() {
      let response = await quizApiService.login();
      if (response.status === 200) {
        this.errorLogin = false;
        this.adminMode = false;
        //save token
      } else {
        this.errorLogin = true;
      }
    }
  },
}

</script>