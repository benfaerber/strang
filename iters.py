def strang_map(function, params, parameter_type, context):
  return [function({
    'context': item,
    'params': params,
    'param_type': parameter_type
  }) for item in context]

def strang_filter(function, params, parameter_type, context):
  return [item for item in context if not not function({
    'context': item,
    'params': params,
    'param_type': parameter_type
  })]

def strang_all(function, params, parameter_type, context):
  return function({
    'context': context,
    'params': params,
    'param_type': parameter_type
  })

def strang_unimpl(function, params, paramter_type, context):
  print('Not Implemented!!!')
  return context

strang_iters = {
  'map': strang_map,
  'filter': strang_filter,
  'reduce': strang_unimpl,
  'every': strang_unimpl,
  'some': strang_unimpl,
  'all': strang_all,
  'unimpl': strang_unimpl
}