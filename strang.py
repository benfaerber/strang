from bs4 import BeautifulSoup

from lexer import StrangLexer

from iters import strang_iters
from std import strang_std

class Strang:
  def __init__(self, raw_code: str, raw_html: str, functional_context: dict):
    lexer = StrangLexer()
    self.lex = lexer.lex(raw_code)
    self.dom = BeautifulSoup(raw_html, 'html.parser')
    self.functional_context = functional_context
    self.variables = {}
    self.constants = {}

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

  def run_function(self, function, context):
    name, params, ptype, ftype = (function[k] for k in ['name', 'params', 'ptype', 'ftype'])

    if name == 'variable' or name == 'let':
      self.variables[params] = context
      return context

    if name == 'constant' or name == 'const':
      is_defined = params in self.constants
      if is_defined:
        raise ValueError(f'Constant "{params}" is already defined!')
      self.constants[params] = context
      return context

    iter_func = strang_iters[ftype]
    func = self.get_function(name)

    new_context = iter_func(func, params, ptype, context)
    return new_context

  def run_block(self, block):
    parent, children = (block[k] for k in ['parent', 'children'])
    node = self.get_node(parent)
    context = node
    for func in children:
      context = self.run_function(func, context)

  def execute(self):
    for block in self.lex:
      self.run_block(block)
