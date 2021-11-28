import re

import std_operators
from std_helpers import destruct, get_attr

def strang_log(data):
  context = destruct(data, 1)
  if 'no_logs' not in data['flags']:
    print(context)
  return context

def strang_plog(data):
  context = destruct(data, 1)
  print(context[0])
  return context

def strang_out(data):
  return data['context']

def string_literal_map(context, params, property_pattern):
  fillins = re.findall(property_pattern, params)
  built = params
  for fillin in fillins:
    built = built.replace(f'$.{fillin}', get_attr(fillin, context))
  return built

def strang_map(data):
  context, params, ptype = destruct(data)
  property_pattern = r'\$(?:\.([a-zA-Z0-9_]+))?'
  if ptype == 'string':
    # TODO: Implement String Map
    return string_literal_map(context, params, property_pattern)

  matches = re.match(property_pattern, params)
  attr = matches and matches.group(1)
  if attr:
    return get_attr(attr, context)

  return context

# String Manipulation

def strang_slice(data):
  context, (rmin, rmax) = destruct(data, 2)
  return context[rmin:rmax]

def strang_split(data):
  context, params = destruct(data, 2)
  return context.split(params)

def strang_join(data):
  context, params = destruct(data, 2)
  return params.join(context)

def strang_first(data):
  context = destruct(data, 1)
  return [context[0]]

def strang_last(data):
  context = destruct(data, 1)
  return [context[-1]]

def strang_chars(data):
  context = destruct(data, 1)
  return [l for l in context[0]]

def strang_contains(data):
  context, params = destruct(data, 2)
  return params in context

def strang_download(data):
  return data['context']

def strang_sum(data):
  context = destruct(data, 1)
  return context + data['acc']

def strang_concat(data):
  context = destruct(data, 1)
  return str(data['acc']) + str(context)

def strang_reverse(data):
  context = destruct(data, 1)
  return context.reverse()

strang_std = {
  'log': strang_log,
  'plog': strang_plog,
  'map': strang_map,
  'out': strang_out,
  'download': strang_download,
  'slice': strang_slice,
  'first': strang_first,
  'last': strang_last,
  'chars': strang_chars,
  'contains': strang_contains,
  'reverse': strang_reverse,
  'concat': strang_concat,
  'split': strang_split,
  'join': strang_join,

  'falsey': std_operators.strang_falsey,
  'truthy': std_operators.strang_truthy,
  'upper': std_operators.strang_upper,
  'lower': std_operators.strang_lower,
  'capitalize': std_operators.strang_capitalize,

  # Comparision
  'lt': std_operators.strang_lt,
  'gt': std_operators.strang_gt,
  'le': std_operators.strang_le,
  'ge': std_operators.strang_ge,
  'eq': std_operators.strang_eq,
  'ne': std_operators.strang_ne,

  # Operations
  'plus': std_operators.strang_plus,
  'minus': std_operators.strang_minus,
  'times': std_operators.strang_times,
  'divide': std_operators.strang_divide,
  'modulo': std_operators.strang_modulo,
  'sum': strang_sum,
  # Conversion
  'int': std_operators.strang_int,
  'float': std_operators.strang_float,
  'str': std_operators.strang_str
}