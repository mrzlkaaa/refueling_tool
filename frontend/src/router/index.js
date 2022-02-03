import {createRouter, createWebHistory} from "vue-router"
import AddRefuel from "../views/AddRefuel.vue"
import Diary from "../views/Diary.vue"
import List from "../views/List.vue"
import Detail from "../views/Detail.vue"

const routes = [
  { path: '/add-refuel',
    name: "AddRefuel",
    component: AddRefuel,
  },
  { path: '/diary',
    name: "Diary",
    component: Diary, 
  },
  { path: '/refuels',
    name: "List",
    component: List,
    children: [{
      path: ":id/detail",
      name: "Detail",
      component: Detail,
      props: true,
    }]
  },
]

const router = createRouter({

  history: createWebHistory(),
  routes,
})

export default router