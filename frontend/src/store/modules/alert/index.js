import getters  from "./getters.js"
import mutations  from "./mutations.js"
import actions  from "./actions.js"

const state = {
    alert:{
        type:null,
        msg: "",
        display: "none",
    },
    modal:{
        type:null,
        msg: "",
        code:"",
        display: false,
        img: false,
    }
}

export default {
    namespaced: true,
    state:()=>(state),
    getters,
    mutations,
    actions,
}