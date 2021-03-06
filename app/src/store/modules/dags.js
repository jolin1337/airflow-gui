import dagsAPI from '@/api/dags'

export default {
  namespaced: true,
  state: () => ({
    all: [],
    selected: null
  }),
  getters: {},
  actions: {
    getAllDags ({ commit }) {
      dagsAPI.getDags().then((dags) => {
        commit('setDags', dags)
      })
    },
    selectDag ({ commit }, dagId) {
      dagsAPI.getDag(dagId).then((dag) => {
        commit('selectDag', dag)
      }).catch(() => commit('deselectDag'))
    },
    saveSelectedDag ({ state }) {
      dagsAPI.saveDag(state.selected)
    }
  },
  mutations: {
    setDags (state, dags) {
      // TODO Validation
      state.all = dags
    },
    selectDag (state, dag) {
      // TODO Validation
      state.selected = dag
    },
    deselectDag (state) {
      state.selected = null
    },
    updateSelectedDag (state, dag) {
      // TODO Validation
      state.selected = dag
    }
  }
}
