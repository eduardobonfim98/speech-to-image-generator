import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'

// Vuetify
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import router from './router'
import VOtpInput from "vue3-otp-input";

const vuetify = createVuetify({
  components,
  directives,
})

createApp(App)
    .use(createPinia())
    .component('v-otp-input', VOtpInput)
    .use(vuetify)
    .use(router)
    .mount('#app')
