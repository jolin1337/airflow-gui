import Vue from 'vue'
import Vuex from 'vuex'
import dags from './modules/dags'
import operators from './modules/operators'
import tasks from './modules/tasks'
import connections from './modules/connections'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    dags,
    operators,
    tasks,
    connections
  }
})
