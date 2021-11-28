import re

import std_operators
from std_helpers import get_attr

def strang_log(data):
  if 'no_logs' not in data.flags:
    print(data.context)
  return data.context

def strang_plog(data):
  print(data.context[0])
  return data.context

def strang_out(data):
  return data.context

def string_literal_map(context, params, property_pattern):
  fillins = re.findall(property_pattern, params)
  built = params
  for fillin in fillins:
    built = built.replace(f'$.{fillin}', get_attr(fillin, context))
  return built

def strang_map(data):
  property_pattern = r'\$(?:\.([a-zA-Z0-9_]+))?'
  if data.ptype == 'string':
    # TODO: Implement String Map
    return string_literal_map(data.context, data.params, property_pattern)

  matches = re.match(property_pattern, data.params)
  attr = matches and matches.group(1)
  if attr:
    return get_attr(attr, data.context)

  return data.context

def strang_range(data):
  rmin, rmax = data.params
  # Reverse Range
  if rmin > rmax:
    range_spread = [rmin - v for v in range(rmin - rmax)]
    return range_spread

  range_spread = [v + rmin for v in range(rmax - rmin)]
  return range_spread

# String Manipulation

def strang_slice(data):
  rmin, rmax = data.params
  return data.context[rmin:rmax]

def strang_split(data):
  return data.context.split(data.params)

def strang_join(data):
  return data.params.join(data.context)

def strang_first(data):
  return [data.context[0]]

def strang_last(data):
  return [data.context[-1]]

def strang_chars(data):
  return [l for l in data.context[0]]

def strang_contains(data):
  return data.params in data.context

def strang_download(data):
  return data.context

def strang_sum(data):
  return data.context + data.acc

def strang_concat(data):
  return str(data.acc) + str(data.context)

def strang_reverse(data):
  return data.context.reverse()

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
  'range': strang_range,

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
  'prepend': std_operators.strang_prepend,
  # Conversion
  'int': std_operators.strang_int,
  'float': std_operators.strang_float,
  'str': std_operators.strang_str
}