<template>
  <div>
    <div id="dag" class="dag-info" v-if="reteDagModel && operators">
      <v-toolbar
        color="#121212"
        small
      >
        <v-toolbar-items class="hidden-sm-and-down">
          <v-btn text @click="saveDag()">
            <v-icon>mdi-content-save</v-icon>
            Save changes
          </v-btn>
          <v-divider vertical></v-divider>
        </v-toolbar-items>
      </v-toolbar>
      <rete v-model="reteDagModel" :operators="operators"/>
    </div>
    <task-instance-properties/>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'
import Rete from '@/components/Rete'
import TaskInstanceProperties from '@/components/TaskInstanceProperties'

export default {
  components: {
    TaskInstanceProperties,
    Rete
  },
  computed: {
    ...mapState({
      dag: state => state.dags.selected,
      operators: state => state.operators.all
    }),
    reteDagModel: {
      get () { return this.dag },
      set (newVal) { this.updateDag(newVal) }
    }
  },
  methods: {
    ...mapMutations({
      deselectDag: 'dags/deselectDag',
      deselectTask: 'tasks/deselectTask',
      updateDag: 'dags/updateSelectedDag'
    }),
    ...mapActions({
      selectDag: 'dags/selectDag',
      getOperators: 'operators/getOperators',
      saveDag: 'dags/saveSelectedDag'
    })
  },
  created () {
    this.selectDag(this.$route.query.dag)
    this.getOperators()
  },
  destroyed () {
    this.deselectDag()
    this.deselectTask()
  }
}
</script>

<style scoped>
.dag-info {
  min-height: calc(100vh - 65px);
}
.dag__action-pane {
  padding: 0 15px;
  max-width: 1785px;
  margin-left: auto;
  margin-right: auto;
}
</style>
