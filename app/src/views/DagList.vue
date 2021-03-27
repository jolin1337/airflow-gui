<template>
  <div class="home">
    <v-banner single-line sticky color="accent">
        <v-row>
          <v-col>
            <v-text-field color="secondary" label="Search dags" v-model="searchTerm">
              <template v-slot:append-outer>
                <v-btn-toggle
                  v-model="dagFilters"
                  multiple
                >
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn v-bind="attrs" v-on="on">
                        <v-icon>mdi-exclamation-thick</v-icon>
                      </v-btn>
                    </template>
                    <span>Filter success dags</span>
                  </v-tooltip>
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn v-bind="attrs" v-on="on">
                        <v-icon>mdi-check</v-icon>
                      </v-btn>
                    </template>
                    <span>Filter failed dags</span>
                  </v-tooltip>
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn v-bind="attrs" v-on="on">
                        <v-icon>mdi-pause</v-icon>
                      </v-btn>
                    </template>
                    <span>Include paused dags</span>
                  </v-tooltip>
                </v-btn-toggle>
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
                </v-menu >
              </template>
            </v-text-field>
          </v-col>
        </v-row>
    </v-banner>
    <v-list>
      <template v-for="dag in filteredDag">
        <div :key="dag.dag_id">
          <v-subheader v-if="dag.header" v-text="dag.header"></v-subheader>
          <dag-list-item :dag="dag" />
          <v-divider :inset="true"></v-divider>
        </div>
      </template>
    </v-list>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import DagListItem from '@/components/DagListItem'

export default {
  data () {
    return {
      searchTerm: '',
      dagFilters: [2]
    }
  },
  components: {
    DagListItem
  },
  computed: {
    ...mapState({
      dags: state => state.dags.all
    }),
    filteredDag () {
      return this.dags.filter(dag => {
        const searchMatch = this.searchTerm === '' || dag.dag_id.includes(this.searchTerm)
        const filterBtns = this.dagFilters.filter(f => {
          switch (f) {
            case 0: // failed tasks
              return dag.dag_runs.find(r => r.state === 'failed')
            case 1: // succeeded tasks
              return dag.dag_runs.length > 0 && !dag.dag_runs.find((r) => r.state === 'failed')
            case 2: // include Paused dags
              return !dag.is_paused
            default:
              return false
          }
        })
        return searchMatch && (this.dagFilters.length === 0 || filterBtns.length > 0)
      })
    }
  },
  methods: {
    ...mapActions({
      getAllDags: 'dags/getAllDags'
    })
  },
  created () {
    this.getAllDags()
  }
}
</script>

<style>
.home {
  min-height: 100vh;
}
</style>
