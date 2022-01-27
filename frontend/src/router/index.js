import {createRouter, createWebHistory} from "vue-router"
import HelloWorld from "../views/HelloWorld.vue"
import Diary from "../views/Diary.vue"

const routes = [
  { path: '/',
    component: HelloWorld,
  },
  { path: '/diary',
    component: Diary, },
]

const router = createRouter({

  history: createWebHistory(),
  routes,
})

export default router