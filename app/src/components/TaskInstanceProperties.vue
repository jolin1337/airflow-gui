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
    </v-navigation-drawer>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex'
export default {
  props: {
    value: Object
  },
  data () {
    return {
      group: 'test2'
    }
  },
  computed: {
    job () { return this.value },
    ...mapState({
      taskId: state => (state.tasks.selected || {}).task_id
    }),
    executedTask () {
      if (!this.job) {
        return
      }
      const run = this.job.executed_tasks.find(e => e.task_id === this.taskId)
      return run
    },
    drawer: {
      get () { return this.job !== null },
      set (val) { val === false && this.deselectTask() }
    }
  },
  methods: {
    ...mapMutations({
      deselectTask: 'tasks/deselectTask'
    })
  },
  mounted () {
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
