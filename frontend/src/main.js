import { createApp } from 'vue'
import { store } from "./vuex"
import App from './App.vue'
import router from './router'

let app = createApp(App)
if (process.env.NODE_ENV === 'development'){
    app.config.globalProperties.procDepHost = "http://localhost:8890"
    app.config.globalProperties.generDepHost = "http://localhost:8001"
    app.config.globalProperties.refuelDepHost = "http://localhost:8888"
    app.config.globalProperties.diaryDepHost = "http://localhost:8889"
    app.config.globalProperties.authDepHost = "http://localhost:8892"
} else {
    app.config.globalProperties.procDepHost = "http://proc.nss-irt-t.xyz:8000"
    app.config.globalProperties.generDepHost = "http://proc.nss-irt-t.xyz:8000"
    app.config.globalProperties.refuelDepHost = "http://refuel.nss-irt-t.xyz:88"
    app.config.globalProperties.diaryDepHost = "http://diary.nss-irt-t.xyz:89"
    app.config.globalProperties.authDepHost = "http://auth.nss-irt-t.xyz:90"
}
app.use(router).use(store).mount('#app')