<template>
  <v-stepper alt-labels v-model="currentRun">
    <v-stepper-header>
      <v-divider v-if="dagRuns.length <= 1"></v-divider>
      <template v-if="dagRuns.length > 0">
        <template v-for="(run, idx) in dagRuns">
            <dag-run-item
              :run-id="run.id"
              :key="idx * 2"
              :state="runState(run)"
              :execution-date="run.task_instances[0].execution_date"
            />
          <v-divider :key="idx * 2 + 1" v-if="idx + 1 < showMaxRuns && idx + 1 < dagRuns.length"></v-divider>
        </template>
      </template>
      <template v-else>
        <dag-run-item />
      </template>
      <v-divider v-if="dagRuns.length <= 1"></v-divider>
    </v-stepper-header>
  </v-stepper>
</template>

<script>
import { mapState } from 'vuex'
import DagRunItem from '@/components/DagRunItem'
export default {
  components: {
    DagRunItem
  },
  props: {
    value: Number
  },
  data () {
    return {
      showMaxRuns: 10
    }
  },
  watch: {
    dagRuns () {
      if (this.currentRun === null && this.dagRuns.length > 0) {
        this.currentRun = this.dagRuns[this.dagRuns.length - 1].id
      }
    }
  },
  computed: {
    currentRun: {
      get () { return this.value },
      set (newVal) { this.$emit('input', newVal) }
    },
    ...mapState({
      dagRuns (state) {
        const dag = state.dags.selected || {}
        const dagRuns = dag.dag_runs || []
        const validRuns = dagRuns.filter(run => {
          return run.task_instances.length > 0
        })

        const earliestRun = Math.max(0, validRuns.length - this.showMaxRuns)
        return validRuns.slice(earliestRun)
      }
    })
  },
  methods: {
    runHasFailed (run) {
      return run.task_instances.find(t => t.state === 'failed') !== undefined
    },
    runIsRunning (run) {
      return run.task_instances.find(t => t.state === 'running') !== undefined
    },
    runState (run) {
      if (this.runIsRunning(run)) {
        return 'running'
      }
      if (this.runHasFailed(run)) {
        return 'failed'
      }
      return 'success'
    }
  }
}
</script>
