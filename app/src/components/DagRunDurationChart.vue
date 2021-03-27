<template>
  <v-lazy
    v-model="durationIsActive"
    :options="{
      threshold: .5
    }"
    transition="fade-transition"
  >
    <div style="position: relative;">
      <v-sparkline
        :value="dagRunDurations"
        :labels="dagRunDurations"
        :show-labels="true"
        color="rgba(255, 100, 100, .7)"
        style="margin-bottom: 35px;"
        height="100"
        padding="24"
        stroke-linecap="round"
        line-width="1"
        :smooth="5"
        auto-draw
      >
      </v-sparkline>
      <v-sparkline
        v-for="(taskRun, idx) in taskRuns"
        :key="taskRun.id"
        style="position:absolute;top:35px;"
        :value="taskRun"
        :labels="taskRun"
        :show-labels="idx === 0 ? true : false"
        color="rgba(255, 255, 255, .7)"
        height="100"
        padding="24"
        stroke-linecap="round"
        line-width="1"
        :smooth="5"
        auto-draw
      >
      </v-sparkline>
    </div>
  </v-lazy>
</template>
<script>
export default {
  props: {
    dagRuns: Array
  },
  data () {
    return {
      durationIsActive: false,
      value: [
        423,
        446,
        675,
        510,
        590,
        610,
        760
      ]
    }
  },
  computed: {
    dagRunDurations () {
      return this.dagRuns.map(dagRun => {
        const duration = dagRun.task_instances.reduce((g, c) => g + c.duration, 0)
        return parseInt(duration * 100) / 100
      })
    },
    taskRuns () {
      const taskRuns = {}
      this.dagRuns.forEach(dagRun => {
        dagRun.task_instances.forEach(task => {
          if (taskRuns[task.task_id] === undefined) {
            taskRuns[task.task_id] = []
          }
          taskRuns[task.task_id].push(parseInt(task.duration * 100) / 100)
        })
      })
      return Object.values(taskRuns)
    }
  }
}
</script>
