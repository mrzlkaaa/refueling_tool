import {createRouter, createWebHistory} from "vue-router"
import AddRefuel from "../views/AddRefuel.vue"
import Diary from "../views/Diary.vue"

const routes = [
  { path: '/add-refuel',
    component: AddRefuel,
  },
  { path: '/diary',
    component: Diary, 
  },
  // { path: '/list',
  //   component: Diary, },
]

const router = createRouter({

  history: createWebHistory(),
  routes,
})

export default router