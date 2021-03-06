import axios from 'axios'
export default {
  async getOperators () {
    const response = await axios.get('/v1/operators')
    return response.data.operators
  }
}
