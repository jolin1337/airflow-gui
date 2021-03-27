<template>
  <v-dialog
    :fullscreen="fullscreen"
    v-model="dialogModel"
    width="500"
    @keypress.enter="confirmAction"
  >
    <template v-slot:activator="{ on, attrs }">
      <slot name="activator" v-bind="{ on, attrs }">
        <v-btn :text="!!dialogMessage" :icon="!dialogMessage && !!dialogIcon" v-bind="attrs" v-on="on">
          <v-icon v-if="dialogIcon">{{dialogIcon}}</v-icon>
          {{dialogMessage}}
        </v-btn>
      </slot>
    </template>
    <v-card>
      <v-card-title v-if="dialogTitle" class="headline yellow darken-2">
        {{dialogTitle}}
        <template v-if="fullscreen">
          <v-spacer></v-spacer>
          <v-btn icon @click="dialogModel=false"><v-icon>mdi-close</v-icon></v-btn>
        </template>
      </v-card-title>

      <v-card-text>
        <slot></slot>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <slot name="actions" v-bind="{ confirmAction }">
          <v-btn
            color="secondary"
            text
            @click="confirmAction"
          >
            {{actionMessage}}
          </v-btn>
        </slot>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    dialogIcon: String,
    fullscreen: Boolean,
    action: {
      type: Function,
      required: true
    },
    actionMessage: {
      type: String,
      default () {
        return 'Confirm'
      }
    },
    dialogTitle: String,
    dialogMessage: String
  },
  data () {
    return {
      dialogModel: false
    }
  },
  methods: {
    confirmAction () {
      const action = this.action()
      if (action && action.then) {
        action.then(() => {
          this.dialogModel = false
        })
      } else {
        this.dialogModel = false
      }
    }
  }
}
</script>
