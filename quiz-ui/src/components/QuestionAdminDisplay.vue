<template>
  <QuestionEdition @question-update="$emit('question-update')" :create="false" :question="question"
    :originalPosition="originalPosition" />
  <button @click="DeleteQuestion">Delete</button>
  <br />
</template>


<script>
import QuestionEdition from './QuestionEdition.vue';

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
      this.$emit("question-update", this.question, true);
    }
  },
  components: { QuestionEdition }
}
</script>