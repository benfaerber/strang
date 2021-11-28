from std_helpers import destruct

def strang_falsey(data):
  return not data['context']

def strang_truthy(data):
  return not not data['context']

def strang_upper(data):
  return data['context'].upper()

def strang_lower(data):
  return data['context'].lower()

def strang_capitalize(data):
  c = data['context']
  return c[0].upper() + c[1:].lower()

def remove_if_str(value, to_remove):
  if type(value) is str:
    return value.replace(to_remove, '')

  return value

def strang_lt(data):
  context, params, ptype = destruct(data)
  return context < params
def strang_gt(data):
  context, params, ptype = destruct(data)
  return context > params

def strang_le(data):
  context, params, ptype = destruct(data)
  return context <= params

def strang_ge(data):
  context, params, ptype = destruct(data)
  return context >= params

def strang_eq(data):
  context, params, ptype = destruct(data)
  return context == params

def strang_ne(data):
  context, params, ptype = destruct(data)
  return context != params

def strang_plus(data):
  context, params, ptype = destruct(data)
  return context + params

def strang_minus(data):
  context, params, ptype = destruct(data)
  return context - params

def strang_times(data):
  context, params, ptype = destruct(data)
  return context * params

def strang_divide(data):
  context, params, ptype = destruct(data)
  return context / params

def strang_modulo(data):
  context, params, ptype = destruct(data)
  return context % params

def strang_int(data):
  context = destruct(data, 1)
  return int(remove_if_str(context, '\n'))

def strang_float(data):
  context = destruct(data, 1)
  return float(remove_if_str(context, '\n'))

def strang_str(data):
  context = destruct(data, 1)
  return str(context)
