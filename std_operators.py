from std_helpers import destruct

def strang_falsey(data):
  return not not data['context']

def strang_truthy(data):
  return not not data['context']

def strang_upper(data):
  return data['context'].upper()

def strang_lower(data):
  return data['context'].lower()

def strang_lt(data):
  context, params = destruct(data, 2)
  return context < int(params)

def strang_gt(data):
  context, params = destruct(data, 2)
  return context > int(params)

def strang_le(data):
  context, params = destruct(data, 2)
  return context <= int(params)

def strang_ge(data):
  context, params = destruct(data, 2)
  return context >= int(params)

def strang_eq(data):
  context, params = destruct(data, 2)
  return context == int(params)

def strang_plus(data):
  context, params = destruct(data, 2)
  return context + int(params)

def strang_minus(data):
  context, params = destruct(data, 2)
  return context - int(params)

def strang_times(data):
  context, params = destruct(data, 2)
  return context * int(params)

def strang_divide(data):
  context, params = destruct(data, 2)
  return context / int(params)

def strang_modulo(data):
  context, params = destruct(data, 2)
  return context % int(params)

def strang_int(data):
  context = destruct(data, 1)
  return int(context.replace('\n', ''))

def strang_float(data):
  context = destruct(data, 1)
  return float(context.replace('\n', ''))

def strang_str(data):
  context = destruct(data, 1)
  return str(context.replace('\n', ''))
