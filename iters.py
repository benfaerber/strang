def c(data, new_context):
  data.context = new_context
  response = data.function(data)

  if data.modifier and data.modifier.type == 'not':
    response = not response
  return response

def strang_map(data):
  return [c(data, item) for item in data.context]

def strang_filter(data):
  return [
    item for item in data.context
    if not not c(data, item)
  ]

def strang_all(data):
  return data.function(data)

def strang_reduce(data):
  for item in data.context:
    acc = c(data, item)

  return [acc]

def get_bool_list(data):
  bool_list = [
    c(data, item)
    for item in data.context
  ]

  return bool_list

def strang_every(data):
  return [all(get_bool_list(data))]

def strang_some(data):
  return [any(get_bool_list(data))]


def strang_unimpl(data):
  print('Not Implemented!!!')
  return data.context

strang_iters = {
  'map': strang_map,
  'filter': strang_filter,
  'reduce': strang_reduce,
  'every': strang_every,
  'some': strang_some,
  'all': strang_all,
  'unimpl': strang_unimpl
}