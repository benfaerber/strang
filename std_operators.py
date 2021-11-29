def strang_falsey(data):
  return not data.context

def strang_truthy(data):
  return not not data.context

def strang_upper(data):
  return data.context.upper()

def strang_lower(data):
  return data.context.lower()

def strang_capitalize(data):
  c = data.context
  return c[0].upper() + c[1:].lower()

def remove_if_str(value, to_remove):
  if type(value) is str:
    return value.replace(to_remove, '')

  return value

def strang_lt(data):
  return data.context < data.params

def strang_gt(data):
  return data.context > data.params

def strang_le(data):
  return data.context <= data.params

def strang_ge(data):
  return data.context >= data.params

def strang_eq(data):
  return data.context == data.params

def strang_ne(data):
  return data.context != data.params

def strang_plus(data):
  return data.context + data.params

def strang_prepend(data):
  return data.params + data.context

def strang_minus(data):
  return data.context - data.params

def strang_times(data):
  return data.context * data.params

def strang_divide(data):
  return data.context / data.params

def strang_modulo(data):
  return data.context % data.params

def strang_int(data):
  return int(remove_if_str(data.context, '\n'))

def strang_float(data):
  return float(remove_if_str(data.context, '\n'))

def strang_str(data):
  return str(data.context)

def strang_swap(data):
  index_a, index_b = data.cells
  cell_a = data.context.get_cell(index_a)
  cell_b = data.context.get_cell(index_b)
  data.context.set_cell(index_a, cell_b)
  data.context.set_cell(index_b, cell_a)
  return data.context
