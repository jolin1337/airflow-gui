<template>
  <div class="socket"
    v-if="socket.name === 'Operator'"
    :class="[type, socket.name, used ? 'used': '', multiple ? 'multi': ''] |kebab"
    :title="socket.name + '\n' + socket.hint">
    <v-icon v-if="used">mdi-play</v-icon>
    <v-icon v-else>mdi-play-outline</v-icon>
  </div>
  <div class="socket"
    v-else
    :class="[type, socket.name, used ? 'used': '', multiple ? 'multi': ''] | kebab"
    :title="socket.name + '\n' + socket.hint"></div>
</template>

<script>
export default {
  props: ['type', 'socket', 'used', 'multiple']
}
</script>

<style>

.node-editor .connection path {
  fill: none;
  stroke: rgb(9, 26, 211);
  stroke-width: 2px;
  pointer-events: none;
}
.node-editor .connection path.active {
  stroke: #aaa;
}
.node-editor .connection.socket-input-operator.socket-output-operator path {
  stroke: white;
}
</style>

<style scoped>
.v-icon {
  color: white;
  margin-top: -12.5px;
  margin-left: -10px;
  font-size: 26pt;
}

.socket {
  display: inline-block;
  cursor: pointer;
  border: 2px solid rgb(9, 26, 211);
  border-radius: 8px;
  width: 16px;
  height: 16px;
  margin: 10px !important;
  vertical-align: middle;
  background: transparent;
  position: relative;
  z-index: 2;
}
.socket.used {
  background: rgb(9, 26, 211);
}
.socket:not(.operator):after {
  content: "";
  position: absolute;
  width: 0;
  height: 0;
  top: 3px;
  left: 16px;
  display: inline-block;
  border-style: solid;
  border-width: 4px 0 4px 2.6666666667px;
  border-color: transparent transparent transparent rgb(9, 26, 211);
}
.socket:hover {
  border: 2px solid #777;
}
.socket.multiple {
  border-color: yellow;
}
.socket.operator {
  background: transparent;
  border: none;
}
</style>
