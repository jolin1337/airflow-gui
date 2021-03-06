import axios from 'axios'
export default {
  async getTask (dagId, taskId) {
    const response = await axios.get(`/v1/dags/${dagId}/tasks/${taskId}`)
    return response.data.task
  }
}
