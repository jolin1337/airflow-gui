import connectionsAPI from '@/api/connections'

export default {
  namespaced: true,
  state: () => ({
    all: null
  }),
  getters: {},
  actions: {
    getAllConnections ({ commit }) {
      connectionsAPI.getConnections().then(connections => {
        commit('setConnections', connections)
      })
    }
  },
  mutations: {
    setConnections (state, connections) {
      // TODO Validation
      state.all = connections
    }
  }
}
