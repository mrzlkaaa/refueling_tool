import Cookies from "js-cookie"
import getters from "./getters.js"
import {store} from "../../../store"

export default {
    async refreshTokens(){
        return new Promise((resolve, reject) => {
            const req = {
                url: `${import.meta.env.VITE_AUTH}/${import.meta.env.VITE_REFRESH}`,
                method: "POST",
                data: {"token": store.getters["auth/isRefresh"]}, //* write via getters
                auth: null, //todo access via getter
            }
            const request = new Request(
                req.url,
                {
                    method: req.method,
                    headers: {
                        "Authorization": req.auth,
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    },
                    body: req.data ? JSON.stringify(req.data) : null
                });
            console.log("trrr")
            // try{
            fetch(request)
                .then(response => response.json())
                .then(results => {
                    console.log(results)
                    let dur = 7

                    //* first of all is clear old tokens stored in cookies
                    console.log(results.refreshToken)
                    Cookies.set("RefreshToken", results.refreshToken, {expires: dur})  
                    Cookies.set("AccessToken", results.accessToken, {expires: dur})
                    
                    resolve("New tokens are stored in cookies")
                })
                .catch(err => reject(err))
                      
        })
    },
    async register({dispatch}, form){
        RegisterForm = new FormData()
        RegisterForm.append(form.user)
        RegisterForm.append(form.password)
        await dispatch.login(RegisterForm)
    },
    async login({commit}, UserForm) {
        Cookies.set("Username", UserForm.Username, {expires: 7})
        Cookies.set("RefreshToken", UserForm.refreshToken, {expires: 7})
        Cookies.set("AccessToken", UserForm.accessToken, {expires: 7})
        commit('setUser')
    },
    async setCookies({commit}){
        commit('setUser')
    },
    async autologgining({getters, commit}) {
        return new Promise((resolve, reject) => {
            // dispatch("logout")
            if (!store.getters["auth/isAuthenticated"] && Cookies.get("Username")) {
                commit('setUser')
                setTimeout(() => resolve(true), 100)
            } else if (store.getters["isAuthenticated"]){
                console.log(store.getters["auth/isAccess"])
                setTimeout(() => resolve(true), 100)
            } else {
                reject("Autorelog is not avaliable")
                //*call alert to inform user
            }
        })
        
    },
    async logout({dispatch, getters, commit}){
        const req = {
            url: `${import.meta.env.VITE_AUTH}/logout`,
            method: "POST",
            data: null,
            auth: store.getters["auth/isAccess"]
            // auth: store.state.auth.accessToken, //todo access via getter
        }
        Cookies.remove("Username")
        Cookies.remove("RefreshToken")
        Cookies.remove("AccessToken")
        commit('logout')
        dispatch("api/makeFetch", req, {root: true})
    },
    // async clearCookies({commit}){
    //     // return new Promise((resolve, reject) => {
    //         Cookies.remove("RefreshToken")
    //         Cookies.remove("AccessToken")
    //         commit('logout')
    //         resolve("Cookies are reset")
    //     // })
        
        
    // }
}