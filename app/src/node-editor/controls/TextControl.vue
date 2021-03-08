<template>
  <div class="text-control" v-if="$vuetify.icons">
    <label :for="'input_' + ikey" class="label">
      {{ikey}}:
    </label>
    <div>
      <v-dialog
        class="field-edit-dialog"
        :fullscreen="true"
        :persistent="true"
        v-model="isDialogShowing"
        transition="scale-transition"
        origin="center center"
        max-width="600"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            color="primary"
            v-bind="attrs"
            v-on="on"
            icon small
          >
            <v-icon class="expand">mdi-expand-all</v-icon>
            <!-- <i aria-hidden="true" class="expand v-icon notranslate mdi theme--light mdi-expand-all"></i> -->
          </v-btn>
        </template>
        <template v-slot:default="dialog">
          <v-card class="text-field-editor">
            <v-toolbar
              color="primary"
              @mousedown.stop.prevent="dialog.value = dialog.value"
            >
              <v-toolbar-title>{{ikey}}</v-toolbar-title>
              <v-spacer></v-spacer>
              <v-toolbar-items>
                <v-btn
                  icon
                  @click="dialog.value = false"
                >
                  <v-icon>mdi-close</v-icon>
                </v-btn>
              </v-toolbar-items>
            </v-toolbar>
            <v-card-text>
              <div class="text-h2 pa-12">
                <v-textarea ref="textarea" :readonly="readonly" @input="change($event)" :auto-grow="true" :full-width="true">
                </v-textarea>
              </div>
            </v-card-text>
          </v-card>
        </template>
      </v-dialog>
      <input
        type="text"
        ref="inputField"
        :id="'input_' + ikey"
        class="input"
        :readonly="readonly"
        :value="stringifiedValue"
        @mousedown.capture.stop=""
        @mousemove.capture.stop=""
        @input="change($event.target.value)"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: ['readonly', 'emitter', 'ikey', 'getData', 'putData'],
  data () {
    return {
      value: 0,
      isDialogShowing: false
    }
  },
  computed: {
    stringifiedValue () {
      if (this.value instanceof Object) {
        return JSON.stringify(this.value, null, 4)
      } else {
        return this.value
      }
    }
  },
  watch: {
    isDialogShowing (newVal) {
      if (newVal === true) {
        let value = this.value
        if (value instanceof Object) {
          value = JSON.stringify(this.value, null, 4)
        }
        setTimeout(() => {
          this.$refs.textarea.value = value
          this.$refs.textarea.innerHTML = value
        }, 100)
      }
    }
  },
  methods: {
    change (value) {
      try {
        if (this.value instanceof Object) {
          value = JSON.parse(value)
        }
        this.value = value
        this.$emit('input', value)
        this.update()
      } catch (e) {
        console.error(e)
      }
    },
    update () {
      if (this.ikey) this.putData(this.ikey, this.value)
      this.emitter.trigger('process')
    }
  },
  mounted () {
    this.value = this.getData(this.ikey)
  }
}
</script>

<style>
.text-control {
  display: grid;
  color: #ddd;
  grid-template-columns: auto 160px;
}
.text-control .label {
  align-self: center;
}
.text-control .v-btn.v-btn--icon .expand {
  font-size: 10pt;
}
.text-control .v-btn.v-btn--icon {
  margin-left: -20px;
  color: white;
  width: 20px;
  height: 20px;
}

.text-control .input {
  border-radius: 4px;
  align-self: center;
  min-width: 150px;
}
.text-control .clear {
  clear: both;
}

.text-control .field-edit-dialog {
  display: inline;
}
</style>
