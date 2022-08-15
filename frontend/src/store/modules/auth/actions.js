import Cookies from "js-cookie"
import getters from "./getters.js"

export default {
    async refreshTokens({dispatch, commit}){ //todo Promise!
        return new Promise((resolve, reject) => {
            const req = {
                url: `${import.meta.env.VITE_AUTH}/${import.meta.env.VITE_REFRESH}`,
                method: "POST",
                data: {"token": this.state.auth.refreshToken}, //* write via getters
                auth: null, //todo access via getter
            }
            const results = dispatch("api/makeFetch", req, {root:true})
            if (results){   
                console.log(results)
                let dur = 7
                Cookies.set("RefreshToken", results.refreshToken, {expires: dur})
                Cookies.set("AccessToken", results.accessToken, {expires: dur})
                commit('setUser')
                setTimeout(() => resolve(true), 500)
                
            }
            dispatch("logout")
            setTimeout(() => reject(false), 500)
        })
        
        
        
        //* turn code to logout and clear cookies to relog
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
    async autologgining({getters, commit}) {
        return new Promise((resolve, reject) => {
            // dispatch("logout")
            if (!getters["isAuthenticated"] && Cookies.get("Username")) {
                commit('setUser')
                setTimeout(() => resolve(true), 100)
            } else if (getters["isAuthenticated"]){
                console.log(getters["isAccess"])
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
            auth: getters["isAccess"]
            // auth: store.state.auth.accessToken, //todo access via getter
        }
        Cookies.remove("Username")
        Cookies.remove("RefreshToken")
        Cookies.remove("AccessToken")
        commit('logout')
        await dispatch("api/makeFetch", req, {root: true})
    }
}