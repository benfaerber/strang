import re

from dataclasses import dataclass
from pprint import pprint

class StrangLexedFunction:
  def __init__(self, ftype: str, name: str, params: str):
    self.ftype = ftype
    self.name = name
    self.params = params
    self.ptype = self.get_ptype(params)

  def get_ptype(self, params: str):
    if not params:
      return 'void'
    is_str = params.startswith('\'') and params.endswith('\'')
    ptype = 'string' if is_str else 'normal'
    return ptype

  def __repr__(self):
    return f'StrangParsedFunction(ftype={self.ftype}, name={self.name}, params={self.params}, ptype={self.ptype})'

  def __str__(self):
    return f'Type: {self.ftype}, Name: {self.name}, Params: {self.params}'

class StrangLexer:
  def __init__(self):
    self.use_tabs = False
    self.tab_size = 2

    self.func_symbols = {
      '-': 'map',
      '~': 'filter',
      '=': 'reduce',
      ':': 'some',
      '!': 'every'
    }

  def count_leading_tabs(self, text):
    text = text.replace('\t', ' ' * self.tab_size)
    count = 0
    for letter in text:
      if letter != ' ':
        break

      count += 1

    return int(count / self.tab_size)

  def lex_function(self, raw_func):
    func_regex = r'(.+)(=|~|-|:|!)>(.+)'
    matches = re.match(func_regex, raw_func)
    if matches:
      func, key, params = (p.strip() for p in matches.groups())
      func_type = self.func_symbols[key]
      return StrangLexedFunction(func_type, func, params)

    return StrangLexedFunction('map', raw_func.strip(), None)

  def lex(self, raw_code):
    lines = raw_code.split('\n')
    lines_not_empty = [l for l in lines if not not l]
    lines_no_comments = [l.split(';')[0] for l in lines_not_empty]

    current_block = 0
    blocks = []
    for line in lines_no_comments:
      tab_size = self.count_leading_tabs(line)
      if tab_size == 0:
        blocks.append({'parent': line, 'children': []})
        current_block = len(blocks) - 1
      else:
        block = blocks[current_block]

        func = self.lex_function(line.strip())
        block['children'].append(func)

    return blocks



def load_strang_code():
  with open('./test.strang', 'r') as file:
    return file.read()

def main():
  strang_code = load_strang_code()
  lexer = StrangLexer()
  blocks = lexer.lex(strang_code)
  pprint(blocks)

if __name__ == '__main__':
  main()