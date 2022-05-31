<template>
  <p>{{ question.title }}</p>
  <p>{{ question.text }}</p>
  <img v-if="question.image" :src="question.image" />
  <a v-for="(answerEntry, index) in question.possibleAnswers" :key="answerEntry.text"
    @click="$emit('answer-selected', index + 1)">
    {{ answerEntry.text }}
  </a>
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