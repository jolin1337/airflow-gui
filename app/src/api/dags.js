import axios from 'axios'
export default {
  async getDags (dagId) {
    let condition = ''
    if (dagId) {
      condition = `(where: { dag_id: { _eq: "${dagId}" } })`
    }
    const data = {
      query: `query api_dags {
        dag${condition} {
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
  async getDagRuns (dagId) {
    const data = {
      query: `query api_dags {
        dag(where: { dag_id: { _eq: "${dagId}" } }) {
          dag_id
          description
          is_active
          is_paused
          is_subdag
          owners
          schedule_interval
          default_view
          jobs {
            id
            executed_tasks {
              state
              task_id
              execution_date
              end_date
              duration
              operator
              start_date
            }
          }
        }
      }`
    }
    const response = await axios.post('/v1/graphql', data)
    if (response.data.data.dag.length > 0) {
      const dag = response.data.data.dag[0]
      dag.jobs.sort((a, b) => {
        return new Date((a.executed_tasks[0] || {}).execution_date) - new Date((b.executed_tasks[0] || {}).execution_date)
      })
      return response.data.data.dag[0]
    }
  },
  async getDagGraph (dagId) {
    const response = await axios.get(`/v1/dags/${dagId}/graph`)
    return response.data.graph
  },
  async saveDagGraph (graph) {
    const response = await axios.post(`/v1/dags/${graph.dag_id}/graph`, { graph })
    return response.data
  },
  async triggerDag (dagId, conf) {
    const response = await axios.post(`/v1/dags/${dagId}/trigger`, { dag_id: dagId, conf })
    return response.data
  }
}
