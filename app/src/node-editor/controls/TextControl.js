import Rete from 'rete'
import VueTextControl from './TextControl.vue'

export class TextControl extends Rete.Control {
  constructor (emitter, key, readonly) {
    super(key)
    this.component = VueTextControl
    this.props = { emitter, ikey: key, readonly }
  }

  putData (key, data) {
    this.setValue(data)
    this.getNode().data[key] = data
  }

  setValue (val) {
    this.data.value = val
    this.vueContext.value = val
  }
}
