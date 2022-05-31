<template>
  <div class="new-quiz">
    <h1>This is an new quiz page</h1>
    <form>
      <p>Saisissez votre nom</p>
      <input type="text" v-model="username" placeholder="UserName">
      <p>{{ username }}</p> 
      <button type="button" @click="startQuiz">Start Quiz</button>
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
export default {
  name: "NewQuizPage",
  data() {
    return {
      username :'',
    };
  },
};
</script>
