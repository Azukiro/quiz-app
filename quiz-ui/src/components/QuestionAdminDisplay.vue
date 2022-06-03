<template>
  <QuestionEdition @question-update="$emit('question-update')" :create="false" :question="question"
    :originalPosition="originalPosition" />
  <button class="btn btn-danger" @click="DeleteQuestion">Supprimer la question</button>
  <br />
</template>


<script>
import QuestionEdition from './QuestionEdition.vue';
import quizApiService from '@/services/QuizApiService';
import adminStorageService from '@/services/AdminStorageService';
export default {
  props: {
    question: {
      type: Object,
      required: true,
    },
    questionsSize: {
      type: Number,
      required: true,
    },
    originalPosition: {
      type: Number,
      required: true,
    },
  },

  emits: ["question-update"],
  methods: {
    DeleteQuestion() {
      quizApiService.deleteQuestion(this.question.position, adminStorageService.getToken())
      this.$emit("question-update", this.question, true);
    }
  },
  components: { QuestionEdition }
}
</script>