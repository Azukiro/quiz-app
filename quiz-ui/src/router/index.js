import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";
import NewQuizPage from "../views/NewQuizPage.vue";
import QuestionPage from "../views/QuestionPage.vue";
import ResultPage from "../views/ResultPage.vue";
import AdminPage from "../views/AdminPage.vue";
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "HomePage",
      component: HomePage,
    },
    {
      path: "/start-new-quiz-page",
      name: "NewQuizPage",
      component: NewQuizPage,
    },
    {
      path: "/questions",
      name: "question",
      component: QuestionPage,
    },
    {
      path: "/result",
      name: "result",
      component: ResultPage,
    },
    {
      path: "/admin",
      name: "admin",
      component: AdminPage,
    },
  ],
});

export default router;
