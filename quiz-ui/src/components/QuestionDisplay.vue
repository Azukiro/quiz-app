<template>
  <p class="mt-5">{{ question.title }}</p>
  <p>{{ question.text }}</p>
  <img class="img-thumbnail" v-if="question.image" :src="question.image" />

  <div class="d-grid gap-2 mt-2 mb-2" v-for="(answerEntry, index) in question.possibleAnswers" :key="answerEntry.text">
    <button class="btn btn-light" @click="$emit('answer-selected', index + 1)">
      {{ answerEntry.text }}
    </button>

  </div>
</template>

<script>
export default {
  props: {
    question: {
      type: Object
    }
  },
  emits: ["answer-selected"],
}
</script>