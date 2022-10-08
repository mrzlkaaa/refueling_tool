import Cookies from "js-cookie"
import {store} from "../../../store"

export default {
    setUser: (state) => { 
        state.user = Cookies.get("Username"), 
        state.refreshToken = Cookies.get("RefreshToken"),
        state.accessToken = Cookies.get("AccessToken")
    },
    logout: (state) => {
        state.user = null
        state.refreshToken = null
        state.accessToken = null
    },
}