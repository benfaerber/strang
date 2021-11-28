import re

import std_operators
from std_helpers import destruct, get_attr

def strang_log(data):
  context = destruct(data, 1)
  print(context)
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
  context, params, param_type = destruct(data)
  property_pattern = r'\$(?:\.([a-zA-Z0-9_]+))?'
  if param_type == 'string':
    # TODO: Implement String Map
    return string_literal_map(context, params, property_pattern)

  matches = re.match(property_pattern, params)
  attr = matches and matches.group(1)
  if attr:
    return get_attr(attr, context)

  return context

# String Manipulation

def strang_slice(data):
  context, params = destruct(data, 2)
  clean_str = params.replace(' ', '')
  delimiter = '..'
  if delimiter in clean_str:
    lower, upper = (int(c) for c in clean_str.split(delimiter))
    return context[lower:upper]

  upper = int(clean_str)
  return context[:upper]

def strang_contains(data):
  context, params = destruct(data, 2)
  return params in context

def strang_download(data):
  return data['context']

strang_std = {
  'log': strang_log,
  'map': strang_map,
  'out': strang_out,
  'download': strang_download,
  'slice': strang_slice,
  'contains': strang_contains,

  'falsey': std_operators.strang_falsey,
  'truthy': std_operators.strang_truthy,
  'upper': std_operators.strang_upper,
  'lower': std_operators.strang_lower,

  # Comparision
  'lt': std_operators.strang_lt,
  'gt': std_operators.strang_gt,
  'le': std_operators.strang_le,
  'ge': std_operators.strang_ge,
  'eq': std_operators.strang_eq,

  # Operations
  'plus': std_operators.strang_plus,
  'minus': std_operators.strang_minus,
  'times': std_operators.strang_times,
  'divide': std_operators.strang_divide,
  'modulo': std_operators.strang_modulo,

  # Conversion
  'int': std_operators.strang_int,
  'float': std_operators.strang_float,
  'str': std_operators.strang_str
}