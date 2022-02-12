from os import name
from bs4 import BeautifulSoup
from collections import namedtuple
from copy import deepcopy

from lexer import StrangLexer
from iters import strang_iters
from std import strang_std
from context import Context
from functioncall import FunctionCall

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

  def get_variable(self, pa):
      table = self.variables if pa.type == 'variable' else self.constants
      if pa.key not in table:
        raise ValueError(f'{pa.type} "{pa.key}" is not defined!')
      return deepcopy(table[pa.key])

  def get_node(self, parent):
    node_getters = {
      'string': lambda pa: [str(pa.key)],
      'list': lambda pa: pa.key,
      'null': lambda pa: [],
      'variable': self.get_variable,
      'constant': self.get_variable
    }

    if parent.type in node_getters:
      return (node_getters[parent.type](parent), parent.type)

    return (self.dom.select(parent.key, href=True), 'node')

  def get_function(self, name):
    if name in strang_std:
      return strang_std[name]

    if name in self.functional_context:
      return self.functional_context[name]

    raise ValueError(f'Invalid Function: "{name}"')

  def define_variable(self, name, context, params):
    is_var = name in self.variable_names
    table = self.variables if is_var else self.constants

    is_defined = params in self.constants
    if not is_var and is_defined:
      raise ValueError(f'Constant "{params}" is already defined!')

    table[params] = deepcopy(context.get_data())
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

    ftype = context.get_cell_type(1)
    return defs[ftype] if ftype in defs else 0

  def run_function(self, lexed_function, context):
    if 'show_functions' in self.flags:
      print(lexed_function)
    f = lexed_function

    # Define Variable
    if f.name in self.definition_names:
      definition = self.define_variable(f.name, context, f.params)
      return definition

    if f.name == 'dlog':
      print(context.get_data())
      return context

    iter_func = strang_iters[f.ftype]
    caller = self.get_function(f.name)
    accumulator = self.get_default_accumulator(context)
    function_call = FunctionCall(function=caller, lexed_function=lexed_function, context=context, acc=accumulator, flags=self.flags)
    if 'show_functions' in self.flags:
      print(function_call)

    from_cell_index, to_cell_index = function_call.cells

    if f.name == 'swap':
      return caller(function_call)

    new_cell = iter_func(function_call)

    context.set_cell(to_cell_index, new_cell)
    return context

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

    node, parent_type = self.get_node(parent)
    complete = parent_type == 'variable' or parent_type == 'constant'
    context = Context(node, complete=complete)
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