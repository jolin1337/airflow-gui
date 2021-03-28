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
          dag_runs {
            id
            task_instances {
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
      dag.dag_runs.sort((a, b) => {
        return new Date((a.task_instances[0] || {}).execution_date) - new Date((b.task_instances[0] || {}).execution_date)
      })
      return response.data.data.dag[0]
    }
  },
  async getDagGraph (dagId) {
    const response = await axios.get(`/v1/dags/${dagId}/graph`)
    return response.data.graph
  },
  async saveDagGraph (graph, options) {
    const response = await axios.post(`/v1/dags/${graph.dag_id}/graph`, { graph, ...options })
    return response.data
  },
  async triggerDag (dagId, conf) {
    const response = await axios.post(`/v1/dags/${dagId}/trigger`, { dag_id: dagId, conf })
    return response.data
  },
  async setPausedDag (dagId, paused) {
    const data = {
      query: `mutation MyMutation {
        update_dag(where: {dag_id: {_eq: "airflow_monitoring"}}, _set: {is_paused: ${paused}}) {
          returning {
            dag_id
            is_paused
          }
        }
      }`
    }
    const response = await axios.post('/v1/graphql', data)
    return response.data.data.update_dag.returning[0]
  }
}
