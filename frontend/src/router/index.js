import {createRouter, createWebHistory} from "vue-router"
import { store } from "../store"
import AddRefuel from "../views/AddRefuel.vue"
import Diary from "../views/Diary.vue"
import List from "../views/List.vue"
import Detail from "../views/Detail.vue"
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"
import Settings from "../views/Settings.vue"
import General from "../views/Settings/General.vue"
import Users from "../views/Settings/Users.vue"
import RefreshToken from "../views/RefreshToken.vue"

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
      path: ":refuelName/detail",
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
  },
  { path: "/refresh",
    name: "RefreshToken",
    component: RefreshToken,
    meta:{requiresAuth: true}
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})


router.beforeEach(async (to, from, next) => {

  if (to.name !== 'Login' && to.meta.requiresAuth && !store.getters["auth/isAccess"]){
    next({name:"Login"})
  }
  else if (to.name == "Login" && store.getters["auth/isAccess"]) {
    store.dispatch("auth/logout")
    next({name:"Login"})
    // next({name:"List"})
  }
  else {
    next()
  }

})

export default router