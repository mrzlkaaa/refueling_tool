import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
// import Vue from "vue"
// mudules are below
import  auth  from "./modules/auth"
import  alert  from "./modules/alert"
// import { api } from "./api"
import  mail  from "./modules/mail"
import router from '../router';
import Cookies from "js-cookie"
//*split api up to many independent modules

const api = {
    namespaced: true,
    state:() => ({
        data: null,
        responseCode: null,
    }),
    actions:{
        async makeFetch({dispatch}, req){ //todo transform into promise
            console.log(req)
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
            try{
                const response = await fetch(request)
                let results = await response.json()
                
                if (response.ok){
                    return results
                }
                let ok = await dispatch('errorsHandler', results)
                console.log(ok)
                //* return recursion?
                // if (!ok) {
                //     console.log(ok)
                //     router.push({name:"Login"})
                // }
                return null
                
            }
            catch (err){
                console.log(err)
                // throw err
            }
        },
        async errorsHandler({dispatch}, msg){ //! must be Promise
            console.log(msg)
            switch (msg){
                
                case "token is expired": //! better to redirect to refreshToken page where vuex comes to play
                    router.push({name:"RefreshToken"})
                    break;
                case "you are not eligible for this service":
                    dispatch("alert/modalWarning", {img:true, msg:msg, code:401}, {root:true})
                    //todo add smth like "contact admin" and form appears
                    break;
                case "Wrong credentials":
                    dispatch("alert/alertError", {msg:msg}, {root:true})
                    break;
                case "User not found":
                    dispatch("alert/alertError", {msg:msg}, {root:true})
                    break;
                case "signature is invalid":
                    router.push({name:"Login"})
                    break;
                default:
                    dispatch("alert/modalError", {msg:msg}, {root:true})
                    
            }
        }
    }
}

const store = createStore({
    modules: {
        auth: auth,
        alert: alert,
        api: api,
        mail:mail
    },
    plugins: [createPersistedState()]
})

export { store }
