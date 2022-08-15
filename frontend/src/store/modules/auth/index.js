import getters  from "./getters.js"
import mutations  from "./mutations.js"
import actions  from "./actions.js"

const state =  {
    user: null,
    refreshToken: null,
    accessToken: null,
}
export default {
    namespaced: true,
    state:()=>(state),
    getters,
    mutations,
    actions
}