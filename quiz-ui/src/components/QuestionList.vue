<template>

  <div class="accordion accordion-flush rounded border border-light" id="accordionQuestion">
    <div class="accordion-item" v-for="(question, index) in questions" :key="index">
      <h2 class="accordion-header" :id="'heading' + question.position">
        <button class="accordion-button bg-dark text-center border" :class="{ 'collapsed': index !== 0 }" type="button"
          data-bs-toggle="collapse" :data-bs-target="'#collapse' + question.position" aria-expanded="true"
          :aria-controls="'collapse' + item" style="color: rgb(226, 226, 226);">
          {{ question.text }}
        </button>
      </h2>
      <div :id="'collapse' + question.position" class="accordion-collapse collapse" :class="{ 'show': index === 0 }"
        :aria-labelledby="'heading' + question.position" data-bs-parent="#accordionQuestion">
        <div class="accordion-body bg-dark">
          <QuestionAdminDisplay :question="question" :questionsSize="size" @question-update="UpdateQuestion"
            :originalPosition="question.position" />
        </div>
      </div>
    </div>
  </div>
















  <!-- <div v-for="(question, index) in questions" :key="index">
    <QuestionAdminDisplay :question="question" :questionsSize="size" @question-update="UpdateQuestion"
      :originalPosition="question.position" />
  </div> -->

  <QuestionEdition v-if="createQuestion" :create="true" @question-update="UpdateQuestion" />
  <button class="btn btn-primary mt-3" v-if="!createQuestion" @click="NewQuestion">Add question</button>


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
      console.log(this.questions)
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