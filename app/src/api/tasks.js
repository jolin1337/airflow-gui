import axios from 'axios'
export default {
  async getTask (dagId, taskId) {
    const response = await axios.get(`/v1/dags/${dagId}/tasks/${taskId}`)
    return response.data.task
  },
  async getTaskLog (dagId, taskId, { executionDate, tryNumber }) {
    const params = {
      execution_date: executionDate,
      try_number: tryNumber,
      metadata: 'null'
    }
    const response = await axios.get(`/v1/dags/${dagId}/tasks/${taskId}/logs`, { params })
    return response.data
  }
}
