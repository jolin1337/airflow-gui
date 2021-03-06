<template>
  <div class="home">
    <v-list>
      <template v-for="dag in dags">
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
import { mapState } from 'vuex'
import DagListItem from '@/components/DagListItem'

export default {
  components: {
    DagListItem
  },
  computed: {
    ...mapState({
      dags: state => state.dags.all
    })
  },
  created () {
    this.$store.dispatch('dags/getAllDags')
  }
}
</script>
