import {createRouter, createWebHistory} from "vue-router"
import { mapGetters } from 'vuex'
import { store } from "../vuex.js" 
import AddRefuel from "../views/AddRefuel.vue"
import Diary from "../views/Diary.vue"
import List from "../views/List.vue"
import Detail from "../views/Detail.vue"
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"
import Settings from "../views/Settings.vue"
import General from "../views/Settings/General.vue"
import Users from "../views/Settings/Users.vue"

const routes = [
  { path: '/add-refuel',
    name: "AddRefuel",
    component: AddRefuel,
    meta:{requiresAuth: true}
  },
  { path: '/diary',
    name: "Diary",
    component: Diary,
    meta:{requiresAuth: true}
  },
  { path: '/refuels',
    name: "List",
    component: List,
    meta:{requiresAuth: true},
    alias: "/",
    children: [{
      path: ":id/detail",
      name: "Detail",
      component: Detail,
      meta:{requiresAuth: true},
      props: true,
    }]
  },
  { path: "/settings",
    name: "Settings",
    component: Settings,
    meta:{requiresAuth: true},
    children: [{
      name: "General",
      component: General,
      path: "/settings/general"
    },{
      name: "Users",
      component: Users,
      meta:{requiresAuth: true},
      path: "/settings/users"
    }]
  },
  { path: "/login",
    name: "Login",
    component: Login,
  },
  { path: "/register",
    name: "Register",
    component: Register,
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {

  store.dispatch('autologgining')

  if (to.name !== 'Login' && to.meta.requiresAuth && !store.state.auth.user){
    next({name:"Login"})
  }
  else if (to.name == "Login" && store.state.auth.user) {
    store.dispatch("logout")
    next({name:"Login"})
  }
  else {
    next()
  }

})

export default router