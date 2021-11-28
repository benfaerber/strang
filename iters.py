def switch_context(data, new_context):
  data['context'] = new_context
  return data

def destruct(data):
  return (data['context'], data['function'])

def strang_map(data):
  context, function = destruct(data)
  return [function(switch_context(data, item)) for item in context]

def strang_filter(data):
  context, function = destruct(data)
  return [
    item for item in context
    if not not function(switch_context(data, item))
  ]

def strang_all(data):
  _, function = destruct(data)
  return function(data)

def strang_reduce(data):
  context, function = destruct(data)
  for item in context:
    acc = function(switch_context(data, item))

  return [acc]

def get_bool_list(data):
  context, function = destruct(data)
  bool_list = [
    function(switch_context(data, item))
    for item in context
  ]

  return bool_list

def strang_every(data):
  return [all(get_bool_list(data))]

def strang_some(data):
  return [any(get_bool_list(data))]


def strang_unimpl(data):
  context, = destruct(data)
  print('Not Implemented!!!')
  return context

strang_iters = {
  'map': strang_map,
  'filter': strang_filter,
  'reduce': strang_reduce,
  'every': strang_every,
  'some': strang_some,
  'all': strang_all,
  'unimpl': strang_unimpl
}