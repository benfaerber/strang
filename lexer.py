import re

from pprint import pprint

strang_symbols = {
  'comment_single_line': ';',
  'comment_multiline_start': '(*',
  'comment_multiline_end': '*)',
  'variable_prefix': '@*',
  'constant_prefix': '@',
  'string_start': '{',
  'string_end': '}'
}

class StrangLexer:
  def __init__(self):
    self.use_tabs = False
    self.tab_size = 2

    self.func_symbols = {
      '-': 'map',
      '=': 'filter',
      '_': 'reduce',
      '.': 'some',
      ':': 'every',
      '|': 'all'
    }

  def parse_params(self, params: str):
    if not params:
      return None, 'void'

    # A range: 0..11
    range_pattern = r'(\d{1,})\.\.(\d{1,})'
    range_match = re.match(range_pattern, params)
    if range_match:
      rmin, rmax = (int(g) for g in range_match.groups())
      return (rmin, rmax), 'range'

    is_str = params.startswith(strang_symbols['string_start']) and params.endswith(strang_symbols['string_end'])
    if is_str:
      slen = len(strang_symbols['string_start'])
      elen = len(strang_symbols['string_end']) * -1
      return params[slen:elen], 'string'

    cleaned_params = params.replace(',', '')
    return cleaned_params, 'normal'


  def count_leading_tabs(self, text):
    text = text.replace('\t', ' ' * self.tab_size)
    count = 0
    for letter in text:
      if letter != ' ':
        break

      count += 1

    return int(count / self.tab_size)

  def count_char(self, text, character):
    count = 0
    for letter in text:
      if letter == character:
        count += 1
    return count

  def lex_parent(self, raw_parent):
    is_var = raw_parent.startswith(strang_symbols['variable_prefix'])
    is_const = raw_parent.startswith(strang_symbols['constant_prefix'])

    str_start = strang_symbols['string_start']
    str_end = strang_symbols['string_end']
    str_literal = raw_parent.startswith(str_start) and raw_parent.endswith(str_end)
    str_count = self.count_char(raw_parent, str_start) == self.count_char(raw_parent, str_end) and self.count_char(raw_parent, str_start) == 1
    is_str = str_literal and str_count

    is_list = not is_str and ',' in raw_parent

    if is_var:
      plen = len(strang_symbols['variable_prefix'])
      return {'type': 'variable', 'selector': raw_parent[plen:]}
    elif is_const:
      plen = len(strang_symbols['constant_prefix'])
      return {'type': 'constant', 'selector': raw_parent[plen:]}
    elif is_str:
      slen = len(strang_symbols['string_start'])
      elen = len(strang_symbols['string_end']) * -1
      return {'type': 'string', 'selector': raw_parent[slen:elen]}
    elif is_list:
      str_list = raw_parent.replace(' ', '').split(',')
      is_str_list = str_start in raw_parent
      convert = lambda v: int(v) if not v.startswith(str_start) else str(v[1:-1])
      convert_list = [convert(s) for s in str_list]
      final_list = [s for s in convert_list if not not s]
      return {'type': 'list', 'selector': final_list}
    elif raw_parent == '!strang':
      return {'type': 'settings', 'selector': 'strang'}

    return {'type': 'node', 'selector': raw_parent}

  def lex_function(self, raw_func):
    func_pattern = r'(.+?)(.)>(.+)?'
    matches = re.match(func_pattern, raw_func)
    if matches:
      groups = matches.groups()
      func, key, params = (None, None, None)

      if None in groups:
        func = groups[0].strip()
        key = groups[1].strip()
        params = '$'
      else:
        func, key, params = (p.strip() for p in groups)

      if key not in self.func_symbols:
        arrow_types = ', '.join([s + '>' for s in self.func_symbols.keys()])
        raise ValueError(f'"{key}>" is not a valid arrow type.\nTry one of the following: "{arrow_types}"')

      func_type = self.func_symbols[key]
      clean_params, param_type = self.parse_params(params)

      lexed_func = {
        'ftype': func_type,
        'ptype': param_type,
        'name': func,
        'params': clean_params
      }

      return lexed_func

    clean_func = raw_func.strip()

    # Variable
    if clean_func.startswith(strang_symbols['constant_prefix']):
      is_var = clean_func.startswith(strang_symbols['variable_prefix'])
      trim_val = len(strang_symbols['variable_prefix' if is_var else 'constant_prefix'])
      params = clean_func[trim_val:]
      clean_params, ptype = self.parse_params(params)

      lexed_func = {
        'ftype': 'map',
        'ptype': ptype,
        'name': 'variable' if is_var else 'constant',
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

  def is_only_whitespace(self, text):
    whitespace = [' ', '\t']
    return all([l in whitespace for l in text])

  def lex(self, raw_code):
    lines = raw_code.split('\n')
    lines_no_comments = [
      l.split(strang_symbols['comment_single_line'])[0]
      for l in lines
    ]

    lines_no_multilines = []
    is_comment = False
    for line in lines_no_comments:
      if strang_symbols['comment_multiline_start'] in line:
        is_comment = True

      if not is_comment:
        lines_no_multilines.append(line)

      if strang_symbols['comment_multiline_end'] in line:
        is_comment = False

    lines_not_empty = [l for l in lines_no_multilines if not self.is_only_whitespace(l)]

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