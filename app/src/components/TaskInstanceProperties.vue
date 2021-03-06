<template>
  <div>
    <v-navigation-drawer class="task-nav-drawer" :value="drawer" right absolute>
      <v-toolbar-title v-if="task">{{task.task_id}}</v-toolbar-title>
      <v-list nav dense>
        <v-list-item-group
          v-model="group"
          active-class="deep-purple--text text--accent-4"
        >
          <v-list-item> <!-- TODO: add @click here -->
            <v-list-item-icon>
              <v-icon>mdi-content-save</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Focus task</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  data () {
    return {
      group: 'test2'
    }
  },
  computed: {
    ...mapState({
      task: state => state.tasks.selected
    }),
    drawer () {
      return !!this.task
    }
  },
  mounted () {
  }
}
</script>

<style scoped>
.task-nav-drawer {
  padding-top: 60px;
}
</style>
