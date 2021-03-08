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
    }
  },
  mutations: {
    selectTask (state, task) {
      // TODO Validation
      state.selected = task
    },
    deselectTask (state) {
      state.selected = null
    }
  }
}
