import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import '@mdi/font/css/materialdesignicons.css'

Vue.use(Vuetify)

const opts = {
  theme: {
    dark: true,
    themes: {
      dark: {
        primary: '#121212',
        secondary: '#b0bec5',
        accent: '#363636',
        error: '#b71c1c'
      },
      light: {
        primary: '#1976D2',
        secondary: '#424242',
        accent: '#82B1FF',
        error: '#FF5252',
        info: '#2196F3',
        success: '#4CAF50',
        warning: '#FFC107'
      }
    }
  }
}

export default new Vuetify(opts)
