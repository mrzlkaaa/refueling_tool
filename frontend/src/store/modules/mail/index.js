import getters  from "./getters.js"
import mutations  from "./mutations.js"
import actions  from "./actions.js"

const state = {
    display: false,
    status: true
}

export default {
    // namespaced: true,
    state:()=>(state),
    getters,
    mutations,
    actions
}