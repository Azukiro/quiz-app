<template>
  <p>{{ question.title }}</p>
  <p>{{ question.text }}</p>
  <img v-if="question.image" :src="question.image" />
  <div v-for="(answerEntry, index) in question.possibleAnswers" v-bind:key="answerEntry.text">
    <a @click="$emit('answer-selected', index + 1)">

      {{ answerEntry.text }}</a>
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