import re

from pprint import pprint

class StrangLexer:
  def __init__(self):
    self.use_tabs = False
    self.tab_size = 2

    self.func_symbols = {
      '-': 'map',
      '=': 'filter',
      '~': 'reduce',
      ':': 'some',
      '!': 'every',
      '|': 'all'
    }

    self.symbols = {
      'comment_single_line': ';',
      'comment_multiline_start': '(*',
      'comment_multiline_end': '*)',
      'variable_prefix': '@',
      'constant_prefix': '@@',
      'string_start': '\'',
      'string_end': '\''
    }

  def get_ptype(self, params: str):
    if not params:
      return 'void'

    is_str = params.startswith(self.symbols['string_start']) and params.endswith(self.symbols['string_end'])
    ptype = 'string' if is_str else 'normal'
    return ptype


  def count_leading_tabs(self, text):
    text = text.replace('\t', ' ' * self.tab_size)
    count = 0
    for letter in text:
      if letter != ' ':
        break

      count += 1

    return int(count / self.tab_size)

  def lex_parent(self, raw_parent):
    is_var = raw_parent.startswith(self.symbols['variable_prefix'])
    is_const = raw_parent.startswith(self.symbols['constant_prefix'])

    if is_const:
      return {'type': 'constant', 'selector': raw_parent[2:]}
    elif is_var:
      return {'type': 'variable', 'selector': raw_parent[1:]}

    return {'type': 'node', 'selector': raw_parent}

  def lex_function(self, raw_func):
    func_regex = r'(.+)(.)>(.+)'
    matches = re.match(func_regex, raw_func)
    if matches:
      func, key, params = (p.strip() for p in matches.groups())
      if key not in self.func_symbols:
        arrow_types = ', '.join([s + '>' for s in self.func_symbols.keys()])
        raise ValueError(f'"{key}>" is not a valid arrow type.\nTry one of the following: "{arrow_types}"')

      func_type = self.func_symbols[key]
      param_type = self.get_ptype(params)

      lexed_func = {
        'ftype': func_type,
        'ptype': param_type,
        'name': func,
        'params': params if param_type != 'string' else params[1:-1]
      }

      if func.endswith('!'):
        lexed_func['name'] = func[:-1]
        lexed_func['not'] = True

      return lexed_func

    clean_func = raw_func.strip()

    # Variable
    if clean_func.startswith(self.symbols['variable_prefix']):
      is_const = clean_func.startswith(self.symbols['constant_prefix'])
      trim_val = 1 if not is_const else 2
      params = clean_func[trim_val:]
      lexed_func = {
        'ftype': 'map',
        'ptype': self.get_ptype(params),
        'name': 'variable' if not is_const else 'constant',
        'params': params
      }
      return lexed_func

    # Void Function
    lexed_func = {
      'ftype': 'map',
      'ptype': 'void',
      'name': raw_func.strip(),
      'params': None
    }
    return lexed_func

  def is_function(self, line):
    arrows = [k + '>' for k in self.func_symbols.keys()]
    for arrow in arrows:
      if arrow in line:
        return True
    return False


  def lex(self, raw_code):
    lines = raw_code.split('\n')
    lines_no_comments = [
      l.split(self.symbols['comment_single_line'])[0]
      for l in lines
    ]

    lines_no_multilines = []
    is_comment = False
    for line in lines_no_comments:
      if self.symbols['comment_multiline_start'] in line:
        is_comment = True

      if not is_comment:
        lines_no_multilines.append(line)

      if self.symbols['comment_multiline_end'] in line:
        is_comment = False

    lines_not_empty = [l for l in lines_no_multilines if not not l]

    current_block = 0
    blocks = []
    for line in lines_not_empty:
      tab_size = self.count_leading_tabs(line)
      if tab_size == 0:
        if self.is_function(line):
          raise ValueError(f'This is note a proper parent!\nLine: "{line}"')

        parent = self.lex_parent(line)
        blocks.append({'parent': parent, 'children': []})
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