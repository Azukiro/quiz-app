
<template>

  <input type="text" v-model="currentQuestion.title" placeholder="Title" />

  <input type="text" v-model="currentQuestion.text" placeholder="Texte" />

  <img v-if="currentQuestion.image" :src="currentQuestion.image" alt="" style="width: 100px;" />

  <input type="number" v-model="currentQuestion.position" placeholder="Position" :max="totalQuestion" min="0" />

  <ImageUpload @file-change="imageFileChangedHandler" />
  <div id="answer">
    <div v-for="(answer, i) in currentQuestion.possibleAnswers" :key="i">
      <input type="text" v-model="answer.text" placeholder="Answer" />
      <input type="radio" :id="i" v-model="selectedAnswer" :value="i" />
    </div>
  </div>
  <button @click="addAnswer">+</button>
  <button v-if="create" @click="addQuestion">Ajouter</button>
  <button v-if="!create" @click="modifyQuestion">Modifier</button>

</template>


<script>
import ImageUpload from '@/components/ImageUpload.vue'
import quizApiService from "@/services/QuizApiService";
import adminStorageService from "@/services/AdminStorageService";
export default {

  data() {
    return {
      totalQuestion: 0,
      currentQuestion: {
        title: '',
        text: '',
        image: '',
        position: 0,
        possibleAnswers: [
          {
            text: '',
            isCorrect: false
          },
        ]
      },
      selectedAnswer: 0,
    }
  },
  props: {
    question: {
      type: Object
    },
    create: {
      type: Boolean,
      default: true
    },
    originalPosition: {
      type: Number,
      required: true,
    },
  },
  emits: ["question-update"],

  components: {
    ImageUpload
  },
  methods: {
    imageFileChangedHandler(file) {
      this.currentQuestion.image = file;
    },
    addAnswer() {
      this.currentQuestion.possibleAnswers.push({
        text: '',
        isCorrect: false
      })
    },

    checkQuestion() {
      if (this.currentQuestion.title && this.currentQuestion.text && this.currentQuestion.possibleAnswers.length > 0) {
        console.log("eee")
        let oneAnswerTrue = false;
        this.currentQuestion.possibleAnswers.forEach(answer => {
          if (answer.isCorrect) {
            oneAnswerTrue = true;
          }
        });
        if (oneAnswerTrue) {
          return true;
        }
        return false;
      }
      console.log(this.currentQuestion.possibleAnswers.length)
      console.log("zzzz")
      return false;
    },
    async addQuestion() {
      this.currentQuestion.possibleAnswers[this.selectedAnswer].isCorrect = true;
      if (!this.checkQuestion()) {
        alert('Veuillez remplir tous les champs');
        return;
      }
      let response = await quizApiService.postQuestion(this.currentQuestion, adminStorageService.getToken());
      console.log(response)
      this.$emit('question-update');
    },
    async modifyQuestion() {
      if (!this.checkQuestion()) {
        alert('Veuillez remplir tous les champs');
        return;
      }
      //currentQuestion possibleAnswers slect good
      for (let index = 0; index < this.currentQuestion.possibleAnswers.length; index++) {
        if (this.selectedAnswer === index) {
          this.currentQuestion.possibleAnswers[index].isCorrect = true;
        } else {
          this.currentQuestion.possibleAnswers[index].isCorrect = false;
        }
      }
      quizApiService.putQuestion(this.originalPosition, this.currentQuestion, adminStorageService.getToken());
      this.$emit('question-update');
    },
  },

  async created() {
    let response = await quizApiService.getQuizInfo();
    this.totalQuestion = response.data.size;
    if (this.question) {
      this.currentQuestion = this.question;
      this.selectedAnswer = this.question.possibleAnswers.findIndex(answer => answer.isCorrect);
    }
  }

}
</script>