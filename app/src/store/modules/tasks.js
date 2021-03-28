import tasksAPI from '@/api/tasks'

export default {
  namespaced: true,
  state: () => ({
    selected: null
  }),
  getters: {},
  actions: {
    selectTask ({ commit, rootState }, taskId) {
      tasksAPI.getTask(rootState.dags.selected.id, taskId).then((task) => {
        commit('selectTask', task)
      }).catch(e => commit('deselectTask'))
    },
    getTaskLog ({ commit, rootState }, { taskId, ...options }) {
      tasksAPI.getTaskLog(rootState.dags.selected.id, taskId, options).then(log => {
        commit('setTaskLog', log)
      })
    }
  },
  mutations: {
    setTaskLog (state, log) {
      const selected = state.selected || {}
      state.selected = {
        ...selected,
        log
      }
    },
    selectTask (state, task) {
      // TODO Validation
      const selected = state.selected || {}
      state.selected = { ...selected, ...task }
    },
    deselectTask (state) {
      state.selected = null
    }
  }
}
