<template>
  <div>
    <div id="dag" class="dag-info" v-if="reteDagModel && operators">
      <v-stepper alt-labels v-model="currentJob">
        <v-stepper-header>
          <v-divider v-if="jobs.length <= 1"></v-divider>
          <template v-if="jobs.length > 0">
            <template v-for="(job, idx) in jobs">
              <dag-job-item
                :key="idx * 2"
                :job-id="job.id"
                :state="jobState(job)"
                :execution-date="job.executed_tasks[0].execution_date"
              />
              <v-divider :key="idx * 2 + 1" v-if="idx + 1 < showMaxRuns && idx + 1 < jobs.length"></v-divider>
            </template>
          </template>
          <template v-else>
            <dag-job-item />
          </template>
          <v-divider v-if="jobs.length <= 1"></v-divider>
        </v-stepper-header>
      </v-stepper>
      <task-instance-properties
        v-if="currentJob"
        :value="task && jobs.find(job => job.id === currentJob)"/>

      <v-banner single-line sticky color="primary">
        <v-toolbar
          color="#121212"
          small
        >
          <v-toolbar-items>
            <v-dialog
              v-model="saveDagDialog"
              width="500"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn tex v-bind="attrs" v-on="on">
                  <v-icon>mdi-content-save</v-icon>
                  Save changes
                </v-btn>
              </template>
              <v-card>
                <v-card-title class="headline yellow darken-2">
                  Save and commit changes
                </v-card-title>

                <v-card-text>
                  <v-checkbox label="Create pull request in Kirby" v-model="createPR"></v-checkbox>
                  Dag name: {{dagId}}
                  <v-textarea v-model="saveDagMessage" color="secondary" label="Commit Message" counter :rules="[rules.length(20)]"></v-textarea>
                </v-card-text>

                <v-divider></v-divider>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="secondary"
                    text
                    @click="validateSaveDag()"
                  >
                    Save &amp; Commit
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-divider vertical></v-divider>

            <v-dialog
              v-model="triggerDagDialog"
              width="500"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn text  v-bind="attrs" v-on="on">
                  <v-icon>mdi-play</v-icon>
                  Trigger DAG
                </v-btn>
              </template>

              <v-card>
                <v-card-title class="headline yellow darken-2">
                  You are about to manually Trigger DAG
                </v-card-title>

                <v-card-text>
                  Dag name: {{dagId}}
                  <v-textarea color="secondary" label="Configuration (JSON)" v-model="triggerDagConfiguration"></v-textarea>
                </v-card-text>

                <v-divider></v-divider>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="secondary"
                    text
                    @click="validatetriggerDag()"
                  >
                    Trigger DAG
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-divider vertical></v-divider>
            <v-btn text>
              <v-icon>mdi-backburger</v-icon>
              Backfill period
            </v-btn>
            <v-divider vertical></v-divider>
          </v-toolbar-items>
        </v-toolbar>
      </v-banner>
      <rete v-model="reteDagModel" :operators="operators"/>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'
import Rete from '@/components/Rete'
import TaskInstanceProperties from '@/components/TaskInstanceProperties'
import DagJobItem from '@/components/DagJobItem'

export default {
  components: {
    TaskInstanceProperties,
    Rete,
    DagJobItem
  },
  data () {
    return {
      showMaxRuns: 10,
      currentJob: null,
      triggerDagDialog: null,
      triggerDagConfiguration: '',
      saveDagDialog: null,
      saveDagMessage: '',
      createPR: false,
      rules: {
        length: len => v => (v || '').length <= len || `Warning, recommended commit messages are max ${len} characters`
      }
    }
  },
  computed: {
    ...mapState({
      task: state => state.tasks.selected,
      dagGraph: state => (state.dags.selected || {}).graph,
      dagRuns: state => (state.dags.selected || {}).runs,
      operators: state => state.operators.all
    }),
    reteDagModel: {
      get () { return this.dagGraph },
      set (newVal) { this.updateDagGraph(newVal) }
    },
    dagId () {
      return (this.dagRuns || {}).dag_id || (this.dagGraph || {}).dag_id
    },
    jobs () {
      if (!this.dagRuns) {
        return []
      }
      const earliestJob = Math.max(0, this.dagRuns.jobs.length - this.showMaxRuns)
      return this.dagRuns.jobs.slice(earliestJob).filter(job => {
        return job.executed_tasks.length > 0
      })
    }
  },
  watch: {
    dagRuns () {
      if (this.currentJob === null && this.jobs.length > 0) {
        this.currentJob = this.jobs[this.jobs.length - 1].id
      }
    }
  },
  methods: {
    jobHasFailed (job) {
      return job.executed_tasks.find(t => t.state === 'failed') !== undefined
    },
    jobIsRunning (job) {
      return job.executed_tasks.find(t => t.state === 'running') !== undefined
    },
    jobState (job) {
      if (this.jobIsRunning(job)) {
        return 'running'
      }
      if (this.jobHasFailed(job)) {
        return 'failed'
      }
      return 'success'
    },
    ...mapMutations({
      deselectDag: 'dags/deselectDag',
      deselectTask: 'tasks/deselectTask',
      updateDagGraph: 'dags/updateSelectedDagGraph'
    }),
    ...mapActions({
      selectDagGraph: 'dags/selectDagGraph',
      selectDagRuns: 'dags/selectDagRuns',
      getOperators: 'operators/getOperators',
      saveDag: 'dags/saveSelectedDag',
      triggerDag: 'dags/triggerDag'
    }),
    validateSaveDag () {
      const options = {
        message: this.saveDagMessage,
        createPR: this.createPR
      }
      this.saveDag(options).then(() => {
        this.dialog = false
        this.saveDagMessage = ''
      })
    },
    validatetriggerDag () {
      this.triggerDag(this.triggerDagConfiguration).then(() => {
        this.dialog = false
        this.triggerDagConfiguration = ''
      })
    }
  },
  created () {
    this.selectDagGraph(this.$route.query.dag)
    this.selectDagRuns(this.$route.query.dag)
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
