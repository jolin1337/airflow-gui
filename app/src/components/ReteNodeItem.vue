<template>
  <div class="node" v-if="$vuetify.icons" :class="[selected(), node.name] | kebab">
    <v-btn icon style="position: absolute;color: white" @click="toggleCompact()">
      <!-- <i aria-hidden="true" :class="['v-icon notranslate mdi theme--light', { 'mdi-chevron-down': compact, 'mdi-chevron-up': !compact }]"></i>-->
      <v-icon v-if="compact">mdi-chevron-down</v-icon>
      <v-icon v-else>mdi-chevron-up</v-icon>
    </v-btn>
    <div :class="['title', stateClass]">
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
  computed: {
    stateClass () {
      if (this.state === 'failed') return 'error'
      return this.state
    }
  },
  data () {
    return {
      compact: true,
      state: null
    }
  },
  components: {
    Socket: /* VueRenderPlugin.Socket */ReteSocket
  }
}
</script>

<style>
.node .title {
  padding-left: 40px;
}

.node-editor .node {
  background-color: rgba(35, 35, 35, 0.7) !important;
  box-shadow: 1px solid black;
  border: 1px solid black;
  border-radius: 10px;
  cursor: pointer;
  display: inline-block;
  height: auto;
  padding-bottom: 6px;
  box-sizing: content-box;
  box-shadow: 4px 5px 9px rgba(0, 0, 0, 0.5);
  min-width: 160px;
}
.node-editor .node:hover {
  background: rgba(35, 35, 35, 0.7);
}
.node-editor .node.selected {
  background: rgba(22, 22, 22, 0.7);
  border: 1px solid #ffd252;
}
.node-editor .node .title {
  border-top: 1px solid #ccc;
  color: white;
  text-align: center;
  font-weight: bold;
  font-family: sans-serif;
  font-size: 18px;
  border-radius: 10px 10px 0 0;
  padding: 8px;
  overflow: hidden;
  background: linear-gradient(to top, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.05) 40%, rgba(255, 255, 255, 0.19) 100%), radial-gradient(70% 40px at center, rgba(0, 255, 0, 0.5) 0%, rgba(0, 255, 0, 0) 60%);
}
.node-editor .node .title.error {
  background: linear-gradient(to top, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.05) 40%, rgba(255, 255, 255, 0.19) 100%), radial-gradient(70% 40px at center, rgba(255, 0, 47, 0.5) 0%, rgba(0, 255, 0, 0) 60%);
}
.node-editor .node .content {
  display: table;
  width: 100%;
}
.node-editor .node .content .col {
  display: table-cell;
  white-space: nowrap;
}
.node-editor .node .content .col:not(:last-child) {
  padding-right: 20px;
}
.node-editor .node .input-title, .node-editor .node .output-title {
  vertical-align: middle;
  color: white;
  display: inline-block;
  font-family: sans-serif;
  font-size: 14px;
  margin: 10px 0;
  line-height: 16px;
}
.node-editor .node .input-control {
  z-index: 1;
  vertical-align: middle;
  display: inline-block;
}
.node-editor .node .input-control, .node-editor .node .output-control {
  width: 100%;
  padding: 10px 18px;
}
.node-editor .node select, .node-editor .node input {
  width: 60px;
  background-color: transparent;
  padding: 2px 6px;
  border: 1px solid white;
  font-size: 14px;
  color: white;
  border-radius: 0;
}

</style>
