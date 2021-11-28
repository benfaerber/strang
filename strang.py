from bs4 import BeautifulSoup

from lexer import StrangLexer
from iters import strang_iters
from std import strang_std

class Strang:
  def __init__(self, raw_code: str, raw_html: str, functional_context: dict = {}, flags: list = []):
    self.lexer = StrangLexer()
    self.lex = self.lexer.lex(raw_code)
    self.dom = BeautifulSoup(raw_html, 'html.parser')
    self.functional_context = functional_context

    self.flags = flags
    self.imported_files = []

    self.variables = {}
    self.constants = {}

    self.variable_names = ['variable', 'let']
    self.constant_names = ['constant', 'const']
    self.definition_names = self.variable_names + self.constant_names

  def get_node(self, parent):
    selector, ptype = (parent[k] for k in ['selector', 'type'])

    if ptype == 'variable':
      if selector not in self.variables:
        raise ValueError(f'Variable "{selector}" is not defined!')
      return self.variables[selector]
    elif ptype == 'constant':
      if selector not in self.constants:
        raise ValueError(f'Constant "{selector}" is not defined!')
      return self.constants[selector]
    elif ptype == 'string':
      return [str(selector)]
    elif ptype == 'list':
      return selector

    return self.dom.select(selector, href=True)

  def get_function(self, name):
    if name in strang_std:
      return strang_std[name]

    if name in self.functional_context:
      return self.functional_context[name]

    raise ValueError(f'Invalid Function: "{name}"')

  def define_variable(self, name, context, params):
    is_var = name in self.variable_names
    if is_var:
      self.variables[params] = context
      return context
    else:
      is_defined = params in self.constants
      if is_defined:
        raise ValueError(f'Constant "{params}" is already defined!')
      self.constants[params] = context
      return context


  def get_default_accumulator(self, context):
    if not context:
      return 0

    defs = {
      int: 0,
      str: '',
      float: 0.0,
      bool: False
    }

    ftype = type(context[0])
    return defs[ftype] if ftype in defs else 0

  def run_function(self, function, context):
    name, params, ptype, ftype = (function[k] for k in ['name', 'params', 'ptype', 'ftype'])

    if name in self.definition_names:
      return self.define_variable(name, context, params)

    iter_func = strang_iters[ftype]
    func = self.get_function(name)

    accumulator = self.get_default_accumulator(context)
    new_context = iter_func({
      'function': func,
      'params': params,
      'ptype': ptype,
      'context': context,
      'acc': accumulator,
      'flags': self.flags
    })
    return new_context

  def reload_dom(self, params, ptype=None):
    print('Not yet implemented!')

  def unset_flag(self, params, ptype):
    if ptype != 'string':
      raise ValueError(f'A flag must be a string!')

    self.flags.remove(params)

  def set_flag(self, params, ptype=None):
    if ptype != 'string':
      raise ValueError(f'A flag must be a string!')

    if params in self.flags:
      return

    self.flags.append(params)

  def import_file(self, params, ptype=None):
    if ptype != 'string':
      raise ValueError(f'Cannot import "{params}". Must be a string!')

    filename = params if params.endswith('.strang') else params + '.strang'
    with open(f'./strang_files/{filename}') as code_file:
      raw_code = code_file.read()
      self.imported_files.append(filename)

      import_lex = self.lexer.lex(raw_code)
      self.lex = import_lex + self.lex

  def set_settings(self, block):
    functions = block['children']
    for function in functions:
      name, params, ptype = (function[k] for k in ['name', 'params', 'ptype'])
      funcs = {
        'load': self.reload_dom,
        'flag': self.set_flag,
        'unflag': self.unset_flag,
        'import': self.import_file
      }

      funcs[name](params, ptype)

  def run_block(self, block):
    parent, children = (block[k] for k in ['parent', 'children'])
    if parent['type'] == 'settings':
      return

    node = self.get_node(parent)
    context = node
    for func in children:
      context = self.run_function(func, context)

  def execute(self):
    for block in self.lex:
      parent = block['parent']
      if parent['type'] == 'settings':
        self.set_settings(block)

    for block in self.lex:
      self.run_block(block)

def main():
  from cli import cli
  cli()

if __name__ == '__main__':
  main()