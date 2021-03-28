import Rete from 'rete'
import VueRenderPlugin from 'rete-vue-render-plugin'
import ConnectionPlugin from 'rete-connection-plugin'
// import DockPlugin from 'rete-dock-plugin'
import AreaPlugin from 'rete-area-plugin'
import ContextMenuPlugin from 'rete-context-menu-plugin'
import AutoArrangePlugin from 'rete-auto-arrange-plugin'
import vuetify from '@/vuetify'
import ReteNodeItem from '@/components/ReteNodeItem'
import ReteMenu from '@/components/ReteMenu'

import { ColorComponent } from '@/node-editor/components/ColorComponent'
import { AFOperatorComponent } from '@/node-editor/components/AFOperatorComponent'

async function setupTasks (editor, tasks) {
  let connections = []
  const nodes = {}
  const rootNodes = []
  let maxConnections = 0
  for (var task of tasks) {
    const node = await editor.getComponent(task.task_type).createNode({ task })
    const downstreams = task.downstream.map(taskId => [taskId, task.task_id])
    connections = connections.concat(downstreams)
    if (downstreams.length > maxConnections) maxConnections = downstreams.length
    if (task.upstream.length > maxConnections) maxConnections = task.upstream.length
    if (task.upstream.length === 0) rootNodes.push(node)
    nodes[task.task_id] = node
    editor.addNode(node)
  }
  connections.forEach(connection => {
    const node1 = nodes[connection[0]]
    const node2 = nodes[connection[1]]
    editor.connect(node2.outputs.get('downstream_tasks'), node1.inputs.get('upstream_tasks'))
  })
  return {
    nodes,
    rootNodes,
    maxConnections
  }
}

export default async function (container, { dag, operators }) {
  var components = [
    new ColorComponent(),
    new AFOperatorComponent(),
    ...operators.map(o => new AFOperatorComponent(o))
  ]
  var editor = new Rete.NodeEditor('demo@0.1.0', container)
  editor.use(ConnectionPlugin)
  editor.use(VueRenderPlugin, {
    component: ReteNodeItem,
    options: {
      vuetify
    }
  })
  editor.use(ContextMenuPlugin, { vueComponent: ReteMenu })
  // editor.use(DockPlugin, {
  //  container: dockContainer,
  //   itemClass: 'dock-item', // default: dock-item
  //   plugins: [VueRenderPlugin] // render plugins
  // })
  editor.use(AreaPlugin)

  var engine = new Rete.Engine('demo@0.1.0')

  components.map(c => {
    editor.register(c)
    engine.register(c)
  })
  editor.on(
    'process nodecreated noderemoved connectioncreated connectionremoved',
    async () => {
      await engine.abort()
      await engine.process(editor.toJSON())
    }
  )
  editor.on('zoom', ({ source }) => {
    return source !== 'dblclick'
  })
  editor.on('nodetranslate', () => {
    return !window.event || !['INPUT', 'LABEL', 'I'].includes(window.event.target.tagName)
  })

  // await editor.fromJSON({})

  editor.view.resize()
  AreaPlugin.zoomAt(editor)

  const { nodes, rootNodes, maxConnections } = await setupTasks(editor, dag.tasks)
  const vertical = maxConnections > 10
  editor.use(AutoArrangePlugin, { margin: { x: 25, y: 25 }, depth: 12, vertical }) // depth - max depth for arrange (0 - unlimited)
  setTimeout(async () => {
    editor.trigger('process')
    Object.values(nodes).forEach(node => editor.view.updateConnections({ node }))
    rootNodes.forEach(node => {
      editor.trigger('arrange', { node: node, vertical })
    })
  }, 1000)

  return {
    editor,
    engine
  }
}
