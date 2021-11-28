from bs4 import BeautifulSoup

from lexer import StrangLexer

from iters import strang_iters
from std import strang_std

class Strang:
  def __init__(self, raw_code: str, raw_html: str, functional_context: dict):
    self.lexer = StrangLexer()
    self.lex = self.lexer.lex(raw_code)
    self.dom = BeautifulSoup(raw_html, 'html.parser')
    self.functional_context = functional_context

    self.flags = []
    self.imported_files = []

    self.variables = {}
    self.constants = {}

    self.variable_names = ['variable', 'let']
    self.constant_names = ['constant', 'const']
    self.definition_names = self.variable_names + self.constant_names

  def get_node(self, parent):
    selector = parent['selector']
    if parent['type'] == 'variable':
      return self.variables[selector]
    elif parent['type'] == 'constant':
      return self.constants[selector]

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


  def run_function(self, function, context):
    name, params, ptype, ftype = (function[k] for k in ['name', 'params', 'ptype', 'ftype'])

    if name in self.definition_names:
      return self.define_variable(name, context, params)

    iter_func = strang_iters[ftype]
    func = self.get_function(name)

    new_context = iter_func(func, params, ptype, context)
    return new_context

  def reload_dom(self, params, ptype=None):
    print('Not yet implemented!')

  def set_flag(self, params, ptype=None):
    if ptype == 'string':
      self.flags.append(params)
    return

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
    parent = block['parent']
    functions = block['children']
    for function in functions:
      name, params, ptype = (function[k] for k in ['name', 'params', 'ptype'])
      funcs = {
        'load': self.reload_dom,
        'flag': self.set_flag,
        'import': self.import_file
      }

      funcs[name](params, ptype)

    return

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
  import sys
  args = sys.argv[1:]
  if len(args) == 0:
    print('You must include a strang file!\nUsage: python strang.py example.strang')
    return

  code_filename = args[0]
  html_filename = 'test.html' if len(args) >= 1 else args[1]

  if not code_filename.endswith('.strang'):
    code_filename += '.strang'

  with open(f'strang_files/{code_filename}', 'r') as code_file, open(f'html/{html_filename}') as html_file:
    raw_code = code_file.read()
    raw_html = html_file.read()
    functional_context = {}
    strang = Strang(raw_code, raw_html, functional_context)
    strang.execute()



if __name__ == '__main__':
  main()