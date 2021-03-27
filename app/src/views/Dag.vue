<template>
  <div>
    <div id="dag" class="dag-info">
      <v-skeleton-loader v-show="!ready"
        type="date-picker, image, image, image"
        class="mb-6 loader"
        :elevation="2"
      ></v-skeleton-loader>
      <div :style="{'visibility': ready ? 'visible' : 'hidden'}" v-if="errorMessage.length === 0">
        <template v-if="reteDagModel && operators">

          <v-parallax :src="image" height="300">
            <edit-dag-button :value="dag" @input="validateSaveDag"/>
            <div class="text-center green--text text-h5">{{dag.description}}</div>

            <remaining-time v-if="dag && dag.schedule_interval" :disabled="dag.is_paused" :cron="scheduleInterval">
            </remaining-time>
          </v-parallax>
          <dag-run-states v-model="currentRun" />
          <task-instance-properties
            v-if="currentRun"
            :value="task && currentDagRunState"/>
          <dag-action-banner/>
          <rete v-model="reteDagModel" :dag-run="currentDagRunState" :operators="operators" @ready="ready=true"/>
          <dag-run-duration-chart v-if="dag && dag.dag_runs" :dag-runs="dag.dag_runs"/>
        </template>
      </div>
      <div v-else>
        <v-alert
          type="error"
          elevation="2">
          <div v-html="errorMessage"></div>
          Go back to the list of existing dags <router-link to="/">here.</router-link>
        </v-alert>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'
import Rete from '@/components/Rete'
import TaskInstanceProperties from '@/components/TaskInstanceProperties'
import DagRunStates from '@/components/DagRunStates'
import DagActionBanner from '@/components/DagActionBanner.vue'
import RemainingTime from '@/components/RemainingTime'
import EditDagButton from '@/components/EditDagButton'
import image from '@/assets/gaming.png'
import DagRunDurationChart from '@/components/DagRunDurationChart.vue'

export default {
  components: {
    TaskInstanceProperties,
    Rete,
    DagRunStates,
    DagActionBanner,
    RemainingTime,
    EditDagButton,
    DagRunDurationChart
  },
  data () {
    return {
      image,
      currentRun: null,
      ready: false,
      innerHeight: window.innerHeight,
      errorMessage: ''
    }
  },
  computed: {
    ...mapState({
      task: state => state.tasks.selected,
      dagGraph: state => (state.dags.selected || {}).graph,
      dag: state => state.dags.selected,
      operators: state => state.operators.all
    }),
    currentDagRunState () {
      const dagRuns = this.dag.dag_runs || []
      return dagRuns.find(dr => dr.id === this.currentRun)
    },
    reteDagModel: {
      get () { return this.dagGraph },
      set (newVal) { this.updateDagGraph(newVal) }
    },
    dagId () {
      return this.$route.query.dag
    },
    scheduleInterval () {
      const cron = this.dag.schedule_interval
      if (cron.startsWith('"') && cron.endsWith('"')) {
        return cron.slice(1, -1)
      } else {
        return null
      }
    },
    dagPausedState () {
      if (this.dag && this.dag.is_paused) {
        return 'OFF'
      }
      return 'ON'
    }
  },
  methods: {
    ...mapMutations({
      deselectDag: 'dags/deselectDag',
      deselectTask: 'tasks/deselectTask',
      updateDagGraph: 'dags/updateSelectedDagGraph'
    }),
    ...mapActions({
      selectDagGraph: 'dags/selectDagGraph',
      selectDagRuns: 'dags/selectDagRuns',
      saveDagGraph: 'dags/saveSelectedDagGraph',
      getOperators: 'operators/getOperators'
    }),
    async validateSaveDag ({ commitMessage, createPR }) {
      const options = {
        message: commitMessage,
        create_pr: createPR
      }
      return await this.saveDagGraph(options)
    },
    toggleDagPaused () {
      this.dag.is_paused = !this.dag.is_paused
      // TODO: Call pause/resume dag API
    }
  },
  created () {
    const dagId = this.$route.query.dag
    this.selectDagGraph(dagId).catch(() => {
      this.errorMessage += `<p>Unable to find DAG graph for ${dagId}</p>`
      this.ready = true
    })
    this.selectDagRuns(dagId).catch(() => {
      this.errorMessage += `<p>Unable to find DAG runs for ${dagId}</p>`
      this.ready = true
    })
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
  position: relative;
}
.dag-info .loader {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.dag__action-pane {
  padding: 0 15px;
  max-width: 1785px;
  margin-left: auto;
  margin-right: auto;
}
</style>
