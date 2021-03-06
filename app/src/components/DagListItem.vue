<template>
  <v-list-item
    @click="$router.push({ path: '/dag', query: { dag: dag.dag_id } })"
  >
    <v-list-item-content>
      <v-list-item-title v-html="dag.dag_id"></v-list-item-title>
      <v-list-item-subtitle v-html="dag.description"></v-list-item-subtitle>
    </v-list-item-content>

    <v-list-item-action v-if="dag.dag_runs">
      <v-btn
        icon
        v-if="dag.dag_runs.reduce((r, g) => g + (r.state === 'failed'), 0) > 1"
      >
        <v-icon color="red lighten-1" class="error-indicator more"
          >mdi-exclamation-thick</v-icon
        >
        <v-icon color="red lighten-1" class="error-indicator more"
          >mdi-exclamation-thick</v-icon
        >
        <v-icon color="red lighten-1" class="error-indicator more"
          >mdi-exclamation-thick</v-icon
        >
      </v-btn>
      <v-btn icon v-else-if="dag.dag_runs.find((r) => r.state === 'failed')">
        <v-icon color="red lighten-1" class="error-indicator"
          >mdi-exclamation-thick</v-icon
        >
      </v-btn>
      <v-btn
        icon
        v-else-if="
          dag.dag_runs.reduce((r, g) => g + (r.state === 'success'), 0) > 0
        "
      >
        <v-icon color="green lighten-1" class="success-indicator"
          >mdi-check</v-icon
        >
      </v-btn>
    </v-list-item-action>
  </v-list-item>
</template>

<script>
export default {
  props: {
    dag: Object
  }
}
</script>

<style scoped>
.success-indicator {
  color: green !important;
}
.error-indicator {
  color: red !important;
}
.error-indicator.more:first-child {
  left: 15px;
}
.error-indicator.more:last-child {
  left: -15px;
}
</style>
