<script setup>
import QuestionManager from '@/components/QuestionManager.vue'
</script>

<template>
  <header>
    <h1> Le QUIZZZZZ </h1>

    <div class="wrapper">
      <QuestionManager />
    </div>
  </header>
</template>


<script>

import participationStorageService from '@/services/ParticipationStorageService';
export default {

  components: {
    QuestionManager
  },

  created() {

    participationStorageService.saveParticipationScore(0);

  }
}
</script>