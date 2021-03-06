import axios from 'axios'
export default {
  async getDags () {
    const data = {
      query: `query api_dags {
        dag {
          dag_id
          description
          is_active
          is_paused
          is_subdag
          owners
          schedule_interval
          default_view
          dag_runs {
            state
            run_id
            execution_date
          }
        }
      }`
    }
    const response = await axios.post('/v1/graphql', data)
    return response.data.data.dag
  },
  async getDag (dagId) {
    const response = await axios.get(`/v1/dags/${dagId}/graph`)
    return response.data.graph
  },
  async saveDag (graph) {
    const response = await axios.post(`/v1/dags/${graph.dag_id}/graph`, { graph })
    return response.data
  }
}
