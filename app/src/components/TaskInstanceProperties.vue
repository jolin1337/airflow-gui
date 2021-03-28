<template>
  <div>
    <v-navigation-drawer class="task-nav-drawer" app right absolute v-model="drawer" expand-on-hover width="45%" :temporary="!drawer" :permanent="drawer"> <!-- TODO: Increase width-->
      <v-toolbar
        dense
        prominent
      >
        <v-toolbar-title>
          <v-btn icon @click="drawer=false"><v-icon>mdi-close</v-icon></v-btn>
          {{taskId}}
        </v-toolbar-title>
      </v-toolbar>
      <template v-if="executedTask">
        <v-alert type="success" v-if="executedTask.state === 'success'">Succeeded run ({{executedTask.execution_date}})</v-alert>
        <v-alert type="error" v-if="executedTask.state === 'failed'">Failed run ({{executedTask.execution_date}})</v-alert>
        <!--<v-sheet :elevation="3" color="teal lighten-3">-->

        <v-banner
        >
          Task execution start: {{executedTask.start_date}}
          Task execution end: {{executedTask.end_date}}
        </v-banner>
      </template>
      <v-list nav dense>
        <v-list-item-group
          v-model="group"
          active-class="text--accent-4"
        >
          <v-list-item> <!-- TODO: add @click here -->
            <v-list-item-icon>
              <v-icon>mdi-content-save</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Focus task</v-list-item-title>
          </v-list-item>
          <v-list-item> <!-- TODO: add @click here -->
            <v-list-item-icon>
              <v-icon>mdi-play</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Clear &amp; Run</v-list-item-title>
          </v-list-item>
          <v-list-item> <!-- TODO: add @click here -->
            <v-list-item-icon>
              <v-icon>mdi-play</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Clear &amp; Run (with dependencies)</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>

      <v-sparkline
        :value="taskRuns.map(t => t.duration || 0)"
        :labels="taskRuns.map(t => (round(t.duration) || 0) + 's')"
        :show-labels="true"
        color="rgba(255, 255, 255, .7)"
        height="100"
        padding="24"
        stroke-linecap="round"
        line-width="1"
        :smooth="5"
        auto-draw
      ></v-sparkline>
      <v-container v-if="log" class="white--text">
        <v-row>
          <v-col align-self="center">
            <h3>Logs:</h3>
          </v-col>
          <v-col cols="auto">
            <v-switch hide-details
              color="primary"
              v-model="wrapLogs"
              inset
              label="Wrap text"
            ></v-switch>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-sheet :class="{ 'text-no-wrap': wrapLogs }" max-height="400" style="overflow: auto" v-html="log.message.split('\n').join('<br/>')">
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-navigation-drawer>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'
export default {
  props: {
    value: Object
  },
  data () {
    return {
      group: 'test2',
      log: undefined,
      wrapLogs: false
    }
  },
  computed: {
    ...mapState({
      task: state => state.tasks.selected,
      taskRuns (state) {
        const dag = state.dags.selected || {}
        const dagRuns = dag.dag_runs || []
        return dagRuns.map(dr => dr.task_instances.find(t => t.task_id === this.taskId)).filter(Boolean)
      }
    }),
    taskId () { return (this.task || {}).task_id },
    run () { return this.value },
    executedTask () {
      if (!this.run) {
        return
      }
      const run = this.run.task_instances.find(e => e.task_id === this.taskId)
      return run
    },
    drawer: {
      get () { return this.run !== null },
      set (val) { val === false && this.deselectTask() }
    }
  },
  methods: {
    ...mapMutations({
      deselectTask: 'tasks/deselectTask'
    }),
    ...mapActions({
      getTaskLog: 'tasks/getTaskLog'
    }),
    round (number, dec = 1000) {
      return parseInt(number * dec) / dec
    },
    updateLog () {
      if (this.taskId) {
        this.getTaskLog({
          taskId: this.taskId,
          executionDate: this.executedTask.execution_date,
          tryNumber: 1
        })
      }
    }
  },
  watch: {
    taskId () {
      this.updateLog()
    },
    'task.log' () {
      this.log = this.task.log
    },
    'executedTask.execution_date' () {
      this.updateLog()
    }
  }
}
</script>

<style scoped>
.task-nav-drawer {
  /* padding-top: 60px; */
  z-index: 100;
  position:fixed;
}

</style>
