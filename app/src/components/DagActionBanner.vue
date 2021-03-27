<template>
  <v-banner single-line sticky color="primary">
    <v-toolbar
      color="#121212"
      small
    >
      <v-toolbar-items>
        <dialog-button
          :action="validateSaveDag"
          action-message="Save &amp; Commit"
          dialog-title="Save and commit changes"
          dialog-icon="mdi-content-save"
          dialog-message="Save changes"
        >
          <v-checkbox color="yellow darken-2" label="Create pull request in Kirby" v-model="createPR"></v-checkbox>
          Dag name: {{dagId}}
          <v-textarea v-model="saveDagMessage" color="secondary" label="Commit Message" counter :rules="[rules.length(20)]"></v-textarea>
        </dialog-button>
        <v-divider vertical></v-divider>

        <dialog-button
          :action="validateTriggerDag"
          action-message="Trigger DAG"
          dialog-title="You are about to manually Trigger DAG"
          dialog-icon="mdi-play"
          dialog-message="Trigger DAG"
        >
          Dag name: {{dagId}}
          <v-textarea color="secondary" label="Configuration (JSON)" v-model="triggerDagConfiguration"></v-textarea>
        </dialog-button>
        <v-divider vertical></v-divider>
        <v-btn text>
          <v-icon>mdi-backburger</v-icon>
          Backfill period
        </v-btn>
        <v-divider vertical></v-divider>
      </v-toolbar-items>
    </v-toolbar>
  </v-banner>
</template>

<script>
import { mapActions } from 'vuex'
import DialogButton from '@/components/DialogButton'

export default {
  components: {
    DialogButton
  },
  props: {
    dagId: String
  },
  data () {
    return {
      createPR: false,
      saveDagMessage: '',
      triggerDagConfiguration: '',
      rules: {
        length: len => v => (v || '').length <= len || `Warning, recommended commit messages are max ${len} characters`
      }
    }
  },
  methods: {
    ...mapActions({
      saveDagGraph: 'dags/saveSelectedDagGraph',
      triggerDag: 'dags/triggerDag'
    }),
    async validateSaveDag () {
      const options = {
        message: this.saveDagMessage,
        create_pr: this.createPR
      }
      await this.saveDagGraph(options).then(() => {
        this.saveDagMessage = ''
      })
    },
    async validateTriggerDag () {
      await this.triggerDag(this.triggerDagConfiguration).then(() => {
        this.triggerDagConfiguration = ''
      })
    }
  }
}
</script>
