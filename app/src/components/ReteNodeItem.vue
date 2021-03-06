<template>
  <div class="node" v-if="$vuetify.icons" :class="[selected(), node.name] | kebab">
    <v-btn icon style="position: absolute;color: white" @click="toggleCompact()">
      <!-- <i aria-hidden="true" :class="['v-icon notranslate mdi theme--light', { 'mdi-chevron-down': compact, 'mdi-chevron-up': !compact }]"></i>-->
      <v-icon v-if="compact">mdi-chevron-down</v-icon>
      <v-icon v-else>mdi-chevron-up</v-icon>
    </v-btn>
    <div class="title">
      {{node.name}}
    </div>
    <div class="content">
      <div class="col" v-if="node.controls.size > 0 || node.inputs.size > 0">
        <template v-for="input in inputs()">
          <div :class="['input', { 'hide': isInputShowing(input) }]"
              :key="input.key"
              style="text-align: left"
              v-show="isInputShowing(input)">
            <Socket
              v-socket:input="input"
              type="input"
              :socket="input.socket"
              :multiple="input.connections.length > 1"
              :used="input.connections.length > 0"/>
            <div class="input-title" v-show="!input.showControl()">{{input.name}}</div>
            <div class="input-control" v-if="input.showControl()" v-control="input.control"></div>
          </div>
        </template>
        <div class="control" v-for="(control, idx) in controls()" v-control="control" v-bind:key="idx"></div>
      </div>
      <div class="col">
        <div class="output" v-for="output in outputs()" :key="output.key">
          <div class="output-title">{{output.name}}</div>
          <Socket
            v-socket:output="output"
            type="output"
            :socket="output.socket"
            :multiple="output.connections.length > 1"
            :used="output.connections.length > 0"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VueRenderPlugin from 'rete-vue-render-plugin'
import ReteSocket from '@/components/ReteSocket'
export default {
  mixins: [VueRenderPlugin.mixin],
  methods: {
    used (io) {
      return io.connections.length
    },
    toggleCompact () {
      this.compact = !this.compact
      this.$nextTick(() => this.editor.view.updateConnections({ node: this.node }))
    },
    isInputShowing (input) {
      const controlHasValue = input.control && input.control.vueContext && input.control.vueContext.value
      return !this.compact || input.connections.length > 0 || controlHasValue || !input.control
    }
  },
  data () {
    return {
      compact: true
    }
  },
  components: {
    Socket: /* VueRenderPlugin.Socket */ReteSocket
  }
}
</script>

<style scoped>
.node .title {
  padding-left: 40px;
}
</style>
