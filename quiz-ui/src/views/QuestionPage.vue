<script setup>
import QuestionManager from '@/components/QuestionManager.vue'
</script>

<template>
  <header>
    <div class="container-sm text-center w-25 mt-5">
      <h1> Le QUIZZZZZ </h1>

      <div class="wrapper">
        <QuestionManager />
      </div>
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