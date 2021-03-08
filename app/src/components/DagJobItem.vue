<template>
  <v-stepper-step
    :step="jobId"
    complete
    editable
    :color="color"
    edit-icon="$complete"
    :rules="[() => state !== 'failed']"
    class="dag-runs"
  >
    <v-tooltip bottom v-if="jobId">
      <template v-slot:activator="{ on, attrs }">
        <small v-bind="attrs" v-on="on">
          <template v-if="state === 'failed'">Failed pipeline run</template>
          <template v-else-if="state === 'running'">Pipeline is currenlty running</template>
          <template v-else-if="state === 'success'">Succcessful pipeline</template>
        </small>
      </template>
      {{executionDate}}
    </v-tooltip>
    <small v-else>No runs for this pipeline is recorded</small>
  </v-stepper-step>
</template>

<script>
export default {
  props: {
    jobId: {
      type: Number,
      default: () => 0
    },
    state: {
      type: String,
      default: () => ''
    },
    executionDate: {
      type: String,
      default: () => ''
    }
  },
  computed: {
    color () {
      switch (this.state) {
        case 'failed': return undefined // Just the default red is good
        case 'running': return 'blue'
        case 'success': return 'green'
        default: return this.jobId ? 'yellow' : 'green'
      }
    }
  }
}
</script>
