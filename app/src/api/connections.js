import axios from 'axios'
export default {
  async getConnections () {
    const data = {
      query: `query api_connections {
        connection {
          id
          conn_id
          conn_type
        }
      }`
    }
    const response = await axios.post('/v1/graphql', data)
    return response.data.data.connection
  }
}
