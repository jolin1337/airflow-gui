import Rete from 'rete'
import { TextControl } from '@/node-editor/controls/TextControl.js'
import * as Socket from '@/node-editor/sockets'
import ReteNodeItem from '@/components/ReteNodeItem'

export class ColorComponent extends Rete.Component {
  constructor () {
    super('Color')
    this.data.component = ReteNodeItem
  }

  builder (node) {
    var in1 = new Rete.Input('colorIn', 'Color', Socket.color, true)
    var out1 = new Rete.Output('colorOut', 'Color', Socket.color, true)
    this.node = node
    in1.addControl(new TextControl(this.editor, 'color'))
    return node
      .addOutput(out1)
      .addInput(in1)
  }

  worker (node, inputs, outputs) {
    if (inputs.colorIn.length === 0) {
      outputs.colorOut = node.data.color || 's'
    } else {
      outputs.colorOut = inputs.colorIn[0] || 's'
    }
    let nodeInstance = null
    if (Object.keys(inputs).filter(input => inputs[input].length === 0).length === 0) {
      const i = Object.keys(inputs).length
      nodeInstance = this.editor.nodes.find(n => n.id === node.id)
      nodeInstance.addInput(new Rete.Input('colorIn' + i, 'Color', Socket.color, true))
    }
    const toRemove = Object.keys(inputs).filter(input => inputs[input].length === 0).slice(1)
    if (toRemove.length > 0 && nodeInstance === null) {
      nodeInstance = this.editor.nodes.find(n => n.id === node.id)
      toRemove.forEach(input => {
        nodeInstance.removeInput(nodeInstance.inputs.get(input))
      })
    }
  }
}
