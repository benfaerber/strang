from os import name
from bs4 import BeautifulSoup
from collections import namedtuple

from lexer import StrangLexer
from iters import strang_iters
from std import strang_std


class FunctionCall:
  def __init__(self, function, lexed_function, context, acc=None, flags=[]):
    self.function = function

    self.params = lexed_function.params
    self.ptype = lexed_function.ptype
    self.modifier = lexed_function.modifier if lexed_function.modifier else None

    self.context = context
    self.acc = acc
    self.flags = flags


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

    self.stats = {}

    self.variable_names = ['variable', 'let']
    self.constant_names = ['constant', 'const']
    self.definition_names = self.variable_names + self.constant_names

  def get_node(self, parent):
    p = parent

    if p.type == 'variable' or p.type == 'constant':
      table = self.variables if p.type == 'variable' else self.constants
      if p.key not in table:
        raise ValueError(f'{p.type} "{p.key}" is not defined!')
      return table[p.key]
    elif p.type == 'string':
      return [str(p.key)]
    elif p.type == 'list':
      return p.key
    elif p.type == 'null':
      return []

    return self.dom.select(p.key, href=True)

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

  def run_function(self, lexed_function, context):
    if 'show_functions' in self.flags:
      print(function)
    f = lexed_function

    if f.name in self.definition_names:
      return self.define_variable(f.name, context, f.params)

    iter_func = strang_iters[f.ftype]
    caller = self.get_function(f.name)

    accumulator = self.get_default_accumulator(context)
    data = FunctionCall(function=caller, lexed_function=lexed_function, context=context, acc=accumulator, flags=self.flags)
    new_context = iter_func(data)
    return new_context

  def reload_dom(self, params, ptype=None):
    print('Not yet implemented!')

  def unset_flag(self, params, ptype):
    if ptype != 'string':
      raise ValueError(f'A flag must be a string!')

    if params in self.flags:
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
    for f in functions:
      funcs = {
        'load': self.reload_dom,
        'flag': self.set_flag,
        'unflag': self.unset_flag,
        'import': self.import_file
      }

      funcs[f.name](f.params, f.ptype)

  def run_block(self, block):
    parent, children = (block[k] for k in ['parent', 'children'])
    if parent.type == 'settings':
      return

    node = self.get_node(parent)
    context = node
    for func in children:
      context = self.run_function(func, context)

  def execute(self):
    for block in self.lex:
      parent = block['parent']
      if parent.type == 'settings':
        self.set_settings(block)

    for block in self.lex:
      self.run_block(block)

    if 'verbose' in self.flags:
      print('VERBOSE OUTPUT:')
      print('  Constants:')
      print('  ', self.constants)
      print('  Variables:')
      print('  ', self.variables)

def main():
  from cli import cli
  cli()

if __name__ == '__main__':
  main()