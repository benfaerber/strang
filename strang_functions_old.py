import re

def strang_log(context, parameters=None):
  print(context)

def strang_out(context, parameters=None):
  return context

def get_attr(attr, c):
  attr_table = {
    'text': c.text,
    'html': c.html,
    'src': c.src
  }

  return attr_table[attr] if attr in attr_table else c.get(attr)

def string_mapper(context, parameters, property_pattern):
  fillins = re.findall(property_pattern, parameters)

  arr = []
  for c in context:
    built = parameters[1:-1]
    for fillin in fillins:
      built = built.replace(f'$.{fillin}', get_attr(fillin, c) or '')
    arr.append(built)
  return arr

def strang_map(context, parameters=None):
  property_pattern = r'\$(?:\.([a-zA-Z0-9_]+))?'
  is_string = parameters.startswith('\'') and parameters.endswith('\'')
  if is_string:
    return string_mapper(context, parameters, property_pattern)

  matches = re.match(property_pattern, parameters)
  attr = matches and matches.group(1)
  if attr:
    return [get_attr(attr, c) for c in context]

  return context

def strang_download(context, parameters=None):
  pass

strang_std = {
  'log': strang_log,
  'map': strang_map,
  'out': strang_out,
  'download': strang_download
}