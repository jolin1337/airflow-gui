import operatorsAPI from '@/api/operators'

export default {
  namespaced: true,
  state: () => ({
    all: []
  }),
  getters: {},
  actions: {
    getOperators ({ commit }) {
      operatorsAPI.getOperators().then((operators) => {
        commit('setOperators', operators)
      })
    }
  },
  mutations: {
    setOperators (state, operators) {
      // TODO Validation
      state.all = operators
    }
  }
}
