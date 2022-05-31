<template>
  <QuestionAdminDisplay v-for="(question, index) in questions" :key="index" :question="question" :questions-size="size"
    @question-update="UpdateQuestion" />
  <QuestionEdition v-if="createQuestion" :create="true" @question-update="UpdateQuestion" />
  <button v-if="!createQuestion" @click="NewQuestion">Add question</button>
</template>


<script>
import quizApiService from '@/services/QuizApiService';
import adminStorageService from "@/services/AdminStorageService";
import QuestionAdminDisplay from '@/components/QuestionAdminDisplay.vue';
import QuestionEdition from './QuestionEdition.vue';
export default {
  data() {
    return {
      questions: [],
      size: 0,
      createQuestion: false
    }
  },
  components: {
    QuestionAdminDisplay,
    QuestionEdition
  },
  methods: {
    async UpdateQuestion() {
      this.createQuestion = false;
      let response = await quizApiService.getQuestions(adminStorageService.getToken());
      this.questions = response.data.questions;
      this.size = response.data.size;
    },
    NewQuestion() {
      this.createQuestion = true;
    }
  },
  created() {
    this.UpdateQuestion()
  },
}
</script>