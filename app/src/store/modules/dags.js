import dagsAPI from '@/api/dags'

export default {
  namespaced: true,
  state: () => ({
    all: [],
    selected: null
  }),
  getters: {},
  actions: {
    async getAllDags ({ commit }) {
      return await dagsAPI.getDags().then((dags) => {
        commit('setDags', dags)
      })
    },
    async selectDagRuns ({ commit }, dagId) {
      return await dagsAPI.getDagRuns(dagId).then(dag => {
        commit('setDagRuns', dag)
      })
    },
    async selectDagGraph ({ commit }, dagId) {
      return await dagsAPI.getDagGraph(dagId).then((dag) => {
        commit('setDagGraph', dag)
      }).catch((e) => {
        commit('deselectDagGraph')
        throw e
      })
    },
    async saveSelectedDagGraph ({ state }, options) {
      return await dagsAPI.saveDagGraph(state.selected.graph, options)
    },
    async saveSelectedDag ({ state }, options) {
      const { graph, dagRuns, ...dag } = state.selected
      return await dagsAPI.saveDag(dag, options)
    },
    async triggerDag ({ state }, configuration) {
      return await dagsAPI.triggerDag(state.selected.id, configuration)
    },
    toggleDag ({ state, commit }) {
      return dagsAPI.setPausedDag(state.selected.id, !state.selected.is_paused).then(resp => {
        console.log(resp)
        commit('setPausedDag', resp.is_paused)
      })
    }
  },
  mutations: {
    setPausedDag (state, paused) {
      state.selected.is_paused = paused
    },
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
        ...runs,
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
