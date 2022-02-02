import {createRouter, createWebHistory} from "vue-router"
import AddRefuel from "../views/AddRefuel.vue"
import Diary from "../views/Diary.vue"
import List from "../views/List.vue"

const routes = [
  { path: '/add-refuel',
    component: AddRefuel,
  },
  { path: '/diary',
    component: Diary, 
  },
  { path: '/refuels',
    component: List, 
    // children: [{
    //   path: "obj",
    //   component: Detail,
    // }]
  },
]

const router = createRouter({

  history: createWebHistory(),
  routes,
})

export default router