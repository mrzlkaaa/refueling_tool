import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vue.prototype.$testDepHost = "http://test.nss-irt-t.xyz"
// Vue.prototype.$refuelDepHost = "http://refuel.nss-irt-t.xyz"
// Vue.prototype.$diaryDepHost = "http://diary.nss-irt-t.xyz"

let app = createApp(App)
// app.config.globalProperties.procDepHost = "http://localhost:8890"
// app.config.globalProperties.refuelDepHost = "http://localhost:8808"
// app.config.globalProperties.diaryDepHost = "http://localhost:8809"
app.config.globalProperties.procDepHost = "http://proc.nss-irt-t.xyz:8000"
app.config.globalProperties.refuelDepHost = "http://refuel.nss-irt-t.xyz:88"
app.config.globalProperties.diaryDepHost = "http://diary.nss-irt-t.xyz:89"
app.use(router).mount('#app')