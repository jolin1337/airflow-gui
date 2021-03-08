<template>
  <div class="home">
    <v-banner single-line sticky color="accent">
        <v-row>
          <v-col>
            <v-text-field color="secondary" label="Search connections" v-model="searchTerm"/>
          </v-col>
          <v-col cols="1" style="text-align: right;">
            <v-menu bottom left offset-y>
              <template v-slot:activator="{ on, attrs }">
                <v-btn v-bind="attrs" v-on="on" icon tab tile large>
                  <v-icon>mdi-chevron-down</v-icon>
                </v-btn>
              </template>
              <v-sheet
                color="primary"
                elevation="1"
                height="300"
                width="300">
                <v-content>
                  <v-row>
                    <v-col>
                      Additional filter stuff
                    </v-col>
                  </v-row>
                </v-content>
              </v-sheet>
            </v-menu ></v-col>
        </v-row>
    </v-banner>
    <v-list>
      <template v-for="conn in filteredConn">
        <div :key="conn.conn_id">
          <v-list-item
            @click="$router.push({ path: '/connection', query: { conn: conn.conn_id } })"
          >
            <v-list-item-content>
              <v-list-item-title v-html="conn.conn_id"></v-list-item-title>
              <v-list-item-subtitle v-html="conn.conn_type"></v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-divider :inset="true"></v-divider>
        </div>
      </template>
    </v-list>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  data () {
    return {
      searchTerm: ''
    }
  },
  components: {
  },
  computed: {
    ...mapState({
      connections: state => state.connections.all
    }),
    filteredConn () {
      if (!this.connections) {
        return []
      }
      return this.connections.filter(conn => {
        const searchMatch = this.searchTerm === '' || conn.conn_id.includes(this.searchTerm)
        return searchMatch
      })
    }
  },
  methods: {
    ...mapActions({
      getAllConnections: 'connections/getAllConnections'
    })
  },
  created () {
    this.getAllConnections()
  }
}
</script>

<style>
.home {
  min-height: 100vh;
}
</style>
