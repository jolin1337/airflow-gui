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
    selectDagRuns ({ commit }, dagId) {
      dagsAPI.getDagRuns(dagId).then(dag => {
        commit('setDagRuns', dag)
      })
    },
    selectDagGraph ({ commit }, dagId) {
      dagsAPI.getDagGraph(dagId).then((dag) => {
        commit('setDagGraph', dag)
      }).catch(() => commit('deselectDagGraph'))
    },
    saveSelectedDag ({ state }) {
      dagsAPI.saveDagGraph(state.selected.graph)
    },
    triggerDag ({ state }, configuration) {
      dagsAPI.triggerDag(state.selected.id, configuration)
    }
  },
  mutations: {
    setDags (state, dags) {
      // TODO Validation
      state.all = dags
    },
    setDagGraph (state, graph) {
      // TODO Validation
      state.selected = {
        id: graph.dag_id,
        graph,
        ...(state.selected || {})
      }
    },
    setDagRuns (state, runs) {
      // TODO Validation
      state.selected = {
        id: runs.dag_id,
        runs,
        ...(state.selected || {})
      }
    },
    deselectDag (state) {
      state.selected = null
    },
    deselectDagGraph (state) {
      const sel = state.selected || {}
      sel.graph = null
    },
    deselectDagRuns (state) {
      const sel = state.selected || {}
      sel.runs = null
    },
    updateSelectedDagGraph (state, dag) {
      // TODO Validation
      const sel = state.selected || {}
      sel.graph = dag
    },
    updateSelectedDagRun (state, dag) {
      // TODO Validation
      const sel = state.selected || {}
      sel.runs = dag
    }
  }
}
