from bs4 import BeautifulSoup

from strang_functions_old import strang_std

class Strang:
  def __init__(self, code, raw_html, function_context={}):
    self.raw_code = code
    self.dom = BeautifulSoup(raw_html, 'html.parser')
    self.function_context = function_context
    self.variables = {}

  def get_node(self, key):
    is_var = key.startswith('@')
    if is_var:
      return

    return self.dom.select(key, href=True)

  def parse_funcs(self, funcs):
    func_lex = []
    for func in funcs:
      cleaned = func.replace(' ->', '->').replace('-> ', '->')
      chunks = cleaned.split('->')
      rep = {'name': chunks[0]}

      has_params = '->' in func
      if has_params:
        rep['parameters'] = chunks[1]

      func_lex.append(rep)

    return func_lex

  def parse_code(self):
    lex = []

    lines = self.raw_code.strip().split('\n')
    clean_lines = [l for l in lines if not l.startswith(';')]
    without_comments = '\n'.join(clean_lines).strip()

    blocks = without_comments.split('\n\n')
    for block in blocks:
      chunks = block.split('\n  ')
      node = chunks[0]
      funcs = chunks[1:]

      lex.append({
        'node': node,
        'functions': self.parse_funcs(funcs)
      })

    return lex

  def run_function(self, context, function):
    name = function['name']


    if name.startswith('@'):
      self.variables[name[1:]] = context
      return

    params = function['parameters'] if 'parameters' in function else None
    is_std = name in strang_std
    is_py = name in self.function_context

    if not is_std and not is_py:
      raise ValueError(f'Invalid Function: {name}')

    func_table = strang_std if is_std else self.function_context
    response = func_table[name](context, params)
    return response

  def execute(self, lex):
    for block in lex:
      node = self.get_node(block['node'])

      context = node
      for function in block['functions']:
        context = self.run_function(context, function)

  def start(self):
    lex = self.parse_code()
    self.execute(lex)