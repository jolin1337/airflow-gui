import Rete from 'rete'
import * as Socket from '@/node-editor/sockets'
import { TextControl } from '@/node-editor/controls/TextControl.js'
import ReteNodeItem from '@/components/ReteNodeItem'

export class AFOperatorComponent extends Rete.Component {
  constructor (operator = { operator_name: 'AFOperator' }) {
    super(operator.operator_name)
    this.operator = operator
    this.data.component = ReteNodeItem
  }

  builder (node) {
    var in1 = new Rete.Input('upstream_tasks', 'Upstream', Socket.operator, true)
    var out1 = new Rete.Output('downstream_tasks', 'Downstream', Socket.operator, true)
    if (this.name === 'AFOperator') {
      node.addControl(new TextControl(this.editor, 'operatorName'))
    }
    node.addOutput(out1)
    node.addInput(in1)

    const args = this.operator.arguments || []
    node.data.operator = this.operator
    args.forEach(arg => {
      const control = new TextControl(this.editor, arg.name, { documentation: this.operator.operator_about })
      const input = new Rete.Input('input_' + arg.name, arg.name, Socket.value, false)
      input.addControl(control)
      node.addInput(input)
    })
    return node
  }

  worker (node, inputs, outputs) {
    if (!node.data.task) {
      node.data.task = {
        task_id: 'new_node_' + node.id,
        task_type: this.name,
        upstream: [],
        downstream: [],
        arguments: {
          kwargs: {
            task_id: `"new_node_${node.id}"`
          }
        }
      }
    }
    const nodeInstance = this.editor.nodes.find(n => n.id === node.id)
    Object.keys(node.data.task.arguments).forEach(key => {
      const input = nodeInstance.inputs.get('input_' + key)
      if (input && !input.control.data.value) {
        input.control.putData(key, node.data.task.arguments[key])
        input.control.setValue(node.data.task.arguments[key])
      }
    })
    node.data.task.upstream = []
    node.data.task.downstream = []
    inputs.upstream_tasks.filter(t => t).forEach(task => {
      node.data.task.upstream.push(task.task_id)
      if (!task.downstream.includes(node.data.task.task_id)) {
        task.downstream.push(node.data.task.task_id)
      }
    })
    outputs.downstream_tasks = node.data.task
    Array.from(nodeInstance.inputs.keys()).forEach(key => {
      const input = inputs[key]
      const id = key.substring(key.indexOf('_') + 1)
      if (key === 'upstream_tasks' || (input instanceof Rete.Input)) return
      if (input.length > 0) {
        node.data.task.arguments[id] = input[0]
      } else {
        const control = nodeInstance.inputs.get(key).control
        node.data.task.arguments[id] = control.getData(id)
      }
    })
  }
}
