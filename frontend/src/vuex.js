import { createStore } from "vuex";
import router from './router';
import Cookies from "js-cookie"

const moduleAuth = {
    state:()=>({
        user: null,
        refreshToken: null,
        accessToken: null, //! not for storing in cookie
    }),
    getters:{
        isAuthenticated: state => state.user,
        isAccess: state => state.accessToken,
        isRefresh: state => state.refreshToken,
    },
    mutations:{
        setUser: (state) => { state.user = Cookies.get("Username"), 
                              state.refreshToken = Cookies.get("RefreshToken"),
                              state.accessToken = Cookies.get("AccessToken")
                            },
        logout: (state) => {state.user = null, state.refreshToken = null, state.accessToken = null},
    },
    actions:{
        async refreshTokens({dispatch, commit}){ //todo rewrite to new fetch style using action
            const req = {
                url: `${import.meta.env.VITE_AUTH}/${import.meta.env.VITE_REFRESH}`,
                method: "POST",
                data: {"token": this.state.auth.refreshToken},
                auth: null, //todo access via getter
            }
            console.log(req.data)
            const results = await dispatch("makeFetch", req)
            if (results){   
                console.log(results)
                let dur = 7
                Cookies.set("RefreshToken", results.refreshToken, {expires: dur})
                Cookies.set("AccessToken", results.accessToken, {expires: dur})
                commit('setUser')
                return true
            }
            return false
        },
        register({dispatch}, form){
            RegisterForm = new FormData()
            RegisterForm.append(form.user)
            RegisterForm.append(form.password)
            dispatch.login(RegisterForm)
        },
        login({commit}, UserForm) {
            Cookies.set("Username", UserForm.Username, {expires: 7})
            Cookies.set("RefreshToken", UserForm.refreshToken, {expires: 7})
            Cookies.set("AccessToken", UserForm.accessToken, {expires: 7})
            commit('setUser')
        },
        autologgining({commit}) {
            commit('setUser')
        },
        async logout({dispatch, commit}){
            const req = {
                url: `${import.meta.env.VITE_AUTH}/logout`,
                method: "POST",
                data: null,
                auth: store.state.auth.accessToken, //todo access via getter
            }
            Cookies.remove("Username")
            Cookies.remove("RefreshToken")
            Cookies.remove("AccessToken")
            commit('logout')
            await dispatch("makeFetch", req)
        },
    }

}

const apiData = {
    state:() => ({
        data: null,
        responseCode: null,
    }),
    actions:{
        async makeFetch({dispatch}, req, fileObj=false){
            console.log(req.data)
            const request = new Request(
            req.url,
            {
                method: req.method,
                headers: {
                    "Authorization": req.auth,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: fileObj ? req.data
                    : req.data ? JSON.stringify(req.data)
                    : null
            });
            try{
                const response = await fetch(request)
                let results = await response.json()
                if (response.ok){
                    return results
                }
                else {
                    let ok = await dispatch('errorsHandler', results)
                    if (ok == false) {
                        router.push({name:"Login"})
                    }
                    else if (ok) {
                        router.go()
                    }
                    return null
                }
                
            }
            catch (err){
                console.log(err)
                // throw err
            }
        },
        async errorsHandler({dispatch}, msg){
            switch (msg){
                case "token is expired":
                    return await dispatch("refreshTokens")
                    // break;
                case "you are not eligible for this service":
                    dispatch("modalWarning", {img:true, msg:msg, code:401})
                    //todo add smth like "contact admin" and form appears
                    break;
                case "Wrong credentials":
                    dispatch("alertError", {msg:msg})
                    break;
                    case "User not found":
                        dispatch("alertError", {msg:msg})
                        break;
                default:
                    dispatch("modalError", {msg:msg})
            }
        }
    }
}

const moduleAlert = {
    state:() => ({
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
    }),
    getters:{
        getAlert:(state) => state.alert,
        getModal:(state) => state.modal
    },
    mutations: {
        hideAlert: (state) => state.alert.display = "none",
        alertSuccess: (state, data) => {
            state.alert.type = "alert alert-success"
            state.alert.img = data.img
            state.alert.msg = data.msg
            state.alert.code = data.code
            state.alert.display = "block"

        },
        alertWarning: (state, data) => {
            // state.alert.type = "alert alert-warning"
            // state.alert.msg = data.msg
            // state.alert.display = "block"
        },
        alertError: (state, data) => {
            state.alert.type = "alert alert-danger"
            state.alert.msg = data.msg
            state.alert.display = "block"
        },
        modalWarning: (state, data) => {

            state.modal.type = "alert alert-warning"
            state.modal.img = data.img
            state.modal.msg = data.msg
            state.modal.code = data.code
            state.modal.display = !state.modal.display
        },
        modalError: (state, data) => {
            state.modal.type = "alert alert-danger"
            state.modal.img = data.img
            state.modal.msg = data.msg
            state.modal.code = data.code
            state.modal.display = !state.modal.display
        },
        resetAlert:(state) => {
            state.alert.type = null
            state.alert.msg = ""
            state.alert.display = "none"
        },
        resetModal:(state) => {
            state.modal.type = null
            state.modal.msg = ""
            state.modal.code = ""
            state.modal.display = false
            state.modal.img = false
        }
    },
    actions: {
        resetAlert({commit}){
            commit("resetAlert")
        },
        resetModal({commit}){
            commit("resetModal")
        },
        hideAlert: ({commit}, duration) => {
            setTimeout(() => {commit('hideAlert')}, 7000)
        },
        alertSuccess({commit}, data) {
            commit("alertSuccess", data)
        },
        alertWarning({commit}, data){
            commit("alertWarning", data)
        },
        alertError({commit}, data){
            commit("alertError", data)
        },
        modalWarning({commit}, data){
            commit("modalWarning", data)
        },
        modalError({commit}, data){
            commit("modalError", data)
        }
    }
}



const mail = {
    state:() => ({
        display: false,
        status: true,

    }),
    getters:{
        isDisplayed:(state) => state.display
    },
    mutations:{
        hideForm(state){
            state.display = false;
        },
        showForm(state){
            state.display = true;
        }
    },
    actions:{
        hideForm({commit}){
            commit("hideForm")
        },
        showForm({commit}){
            commit("showForm")
        }
    }
}

const store = createStore({
    modules: {
        auth: moduleAuth,
        alert: moduleAlert,
        // alert: {
        //     namespaced:true,
        //     state:moduleAlert.state,
        //     getters:moduleAlert.getters,
        //     mutations:moduleAlert.mutations,
        //     actions:moduleAlert.actions
        // },
        api: apiData,
        mail:mail
    }
})

export  { store }