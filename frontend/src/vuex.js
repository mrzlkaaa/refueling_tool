import { createStore } from "vuex";
import Cookies from "js-cookie"

const moduleAuth = {
    state:()=>({
        user: null,
        refreshToken: null,
        accessToken: null, //! not for storing in cookie
    }),
    getters:{
        isAuthenticated: state => state.user,
        isTokenized: state => state.accessToken,
    },
    mutations:{
        setUser: (state) => { state.user = Cookies.get("Username"), 
                              state.refreshToken = Cookies.get("RefreshToken"),
                              state.accessToken = Cookies.get("AccessToken")},
        logout: (state) => {state.user = null, state.refreshToken = null, state.accessToken = null},
    },
    actions:{
        refreshTokens({commit}, server){
            const req = new Request(`${server}/${import.meta.env.VITE_REFRESH}`,
            {
                method: "POST",
                headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                },
                body: JSON.stringify({"token":this.state.refreshToken})
            })

            fetch(req)
                .then(response => response.json())
                .then(data => {
                    let dur = 7
                    Cookies.set("RefreshToken", data.refreshToken, {expires: dur})
                    Cookies.set("AccessToken", data.accessToken, {expires: dur})
                    commit('setUser')
                    setTimeout(this.$router.push, 1000, {name:"List"})
                    // this.$store.dispatch('refreshTokens', data)
                })
                .catch(err => {console.log(err), this.$router.push({name:"Login"})})
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
        logout({commit}){
            Cookies.remove("Username")
            Cookies.remove("RefreshToken")
            Cookies.remove("AccessToken")
            commit('logout')
        },
    }

}

const moduleAlert = {
    state:() => ({
        alert:{
            type:null,
            msg: "",
            code:"",
            display: "none",
            img: false,
        }
    }),
    getters:{
        getAlert:(state) => state.alert
    },
    mutations: {
        hideAlert: (state) => state.alert.display = "none",
        alertSuccess: (state, data) => {
            state.alert.type = "alert alert-success"
            state.alert.msg = data.msg
            state.alert.code = data.code
            state.alert.display = true

        },
        alertWarning: (state, data) => {
            state.alert.type = "alert alert-warning"
            state.alert.msg = data.msg
            state.alert.code = data.code
            state.alert.display = true
        },
        alertError: (state, data) => {
            state.alert.type = "alert alert-danger"
            state.alert.img = data.img
            state.alert.msg = data.msg
            state.alert.code = data.code
            state.alert.display = "block"
            
        }
    },
    actions: {
        hideAlert: ({commit}) => {
            setTimeout(() => {commit('hideAlert')}, 5000)
        },
        alertSuccess({commit}, data) {
            commit("alertSuccess", data)
        },
        alertWarning({commit}, data){
            commit("alertWarning", data)
        },
        alertError({commit}, data){
            console.log(data)
            commit("alertError", data)
        }
    }
}

const apiData = {
    state:() => ({
        data: null,
        responseCode: null,
    }),
    actions:{
        async makeFetch({dispatch}, req){
            const request = new Request(
                req.url,
                {
                    method: req.method,
                    headers: {
                            "Authorization": req.authorization,
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                            },
                    body: req.data ? JSON.stringify(req.data) : null
                });
            const response = await fetch(request)
            return response
            // await dispatch('handleFetch', response)
        },
        makeDataFetch({dispatch}, req){
            const request = new Request(
                req.url,
                {
                    method: req.method,
                    headers: {
                            "Authorization": req.authorization,
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                            },
                    body: req.data ? JSON.stringify(req.data) : null
                });
            const response = await fetch(request)
        }
        // async handleFetch({dispatch}, response) {
        //     if (!response.ok && response.status=="401") {
        //         let results = await response.json()
        //         console.log(results)
        //     }
        // }
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
    }
})

export  { store }