<template>
  <div class="editor">
    <div class="container">
      <div id="rete" class="rete node-editor" ref="rete"></div>
    </div>
    <div class="dock" ref="dock"></div>
  </div>
</template>

<script>
import { mapActions, mapMutations, mapState } from 'vuex'
import init from '@/node-editor'

export default {
  props: {
    value: Object,
    operators: Array
  },
  data () {
    return {
      rete: null,
      selectedTask: null
    }
  },
  computed: {
    ...mapState({
      dagRuns: state => (state.dags.selected || {}).runs
    })
  },
  watch: {
    dagRuns () {
      this.updateDagRunStates()
    },
    operators () {
      this.initRete()
    }
  },
  methods: {
    ...mapMutations({
      deselectTask: 'tasks/deselectTask'
    }),
    ...mapActions({
      selectTask: 'tasks/selectTask'
    }),
    async initRete () {
      if (!this.rete && this.operators) {
        this.rete = await init(this.$refs.rete, {
          dag: this.value,
          dockContainer: this.$refs.dock,
          operators: this.operators
        })
        this.rete.editor.on('nodeselected', (node) => {
          if (!node.data.task) {
            this.selectedTask = null
            this.deselectTask()
          } else {
            this.selectedTask = node.data.task.task_id
            this.selectTask(this.selectedTask)
          }
          this.updateDagRunStates()
        })
        let timeoutId = null
        this.rete.editor.on('process nodetranslated nodecreated noderemoved connectioncreated connectionremoved', () => {
          if (timeoutId !== null) {
            clearTimeout(timeoutId)
          }
          timeoutId = setTimeout(() => {
            const reteJson = this.rete.editor.toJSON()
            const operators = Object.values(reteJson.nodes).filter(node => node.data.task)
            const tasks = operators.map(node => {
              return {
                meta: {
                  position: node.position,
                  id: node.id
                },
                ...node.data.task
              }
            })
            this.$emit('input', {
              ...this.value,
              tasks
            })
            timeoutId = null
          }, 1000)
          this.updateDagRunStates()
        })
      } else {
        // TODO: Lazyload new operators and update old ones
      }
    },
    updateDagRunStates () {
      if (this.rete && this.dagRuns) {
        this.dagRuns.jobs.forEach(run => {
          run.executed_tasks.forEach(taskInstance => {
            const node = this.rete.editor.nodes.find(node => (node.data.task || {}).task_id === taskInstance.task_id)
            if (node) {
              node.vueContext.state = taskInstance.state
            }
          })
        })
      }
    }
  },
  mounted () {
    this.initRete()
  }
}
</script>

<style scoped>
.rete {
  background-size: 20px 20px;
  background-image: linear-gradient(to right, #363636 1px, transparent 1px), linear-gradient(to bottom, #363636 1px, transparent 1px) !important;
  background-color: #272727 !important;
  overflow: hidden !important;
}

.node-editor * {
  box-sizing: border-box;
}
.rete .node .control input, .node .input-control input {
  width: 140px;
}

.rete .node .input {
  margin-top: 5px;
}
.rete .node .input .input-control{
  line-height: 22px;
}

.rete .node .input .text-control .input {
  margin-top: 0;
}
.rete .node .socket.input, .socket.output {
  width: 16px;
  height: 16px;
  border-radius: 8px;
  margin-left: -8px;
  margin-top: 8px;
}
.rete .socket.input.operator {
  background: yellow;
}
.rete .socket.input.value {
  background: grey;
}

select, input {
  width: 100%;
  background-color: white;
  padding: 2px 6px;
  border: 1px solid #ddd;
  font-size: 110%;
  width: 170px;
}

/* Rete Dock operators */
.editor {
    display: flex;
    flex-wrap: nowrap;
    flex-direction: column;
    height: 100vh;
    padding: 0 24px;
}

.dock {
    height: 100px;
    overflow-x: auto;
    overflow-y: hidden;
    white-space: nowrap;
}

.item {
    display: inline-block;
    vertical-align: top;
    transform: scale(0.8);
    transform-origin: 50% 0;
}

.container {
    flex: 1;
    overflow: hidden;
    padding: 0;
    display: inline-block;
    max-width: initial;
}
</style>
