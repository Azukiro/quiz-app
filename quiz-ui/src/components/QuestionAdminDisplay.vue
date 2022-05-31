<template>
  <QuestionEdition @question-update="$emit('question-update')" :create="false" :question="question" />
  <button @click="DeleteQuestion">Delete</button>
</template>


<script>

export default {

  props: {
    question: {
      type: Object,
      required: true,
    }
  },
  emits: ["question-update"],
  methods: {
    DeleteQuestion() {
      this.$emit("question-update", this.question, true);
    }
  }
}
</script>