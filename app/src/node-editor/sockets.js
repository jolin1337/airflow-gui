import { Socket } from 'rete'

const value = new Socket('Value')
const color = new Socket('Color')
const operator = new Socket('Operator')
value.hint = 'Override the input value with a computed value'
operator.hint = 'Dependenies of the operator'

value.combineWith(color)
color.combineWith(value)

export { value, color, operator }
