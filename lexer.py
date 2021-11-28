import re
from pprint import pprint
from collections import namedtuple

strang_symbols = {
  'comment_single_line': ';',
  'comment_multiline_start': '(*',
  'comment_multiline_end': '*)',
  'variable_prefix': '@*',
  'constant_prefix': '@',
  'string_start': '{',
  'string_end': '}',
  'modifier_not': '!',
  'cell_prefix': 'c',
  'cell_pointer': '>'
}

LexedParent = namedtuple('LexedParent', ['type', 'key'])
LexedFunction = namedtuple('LexedFunction', ['name', 'ftype', 'params', 'ptype', 'modifier'], defaults=(None, None, None, 'void', None))
LexedModifier = namedtuple('LexedModifier', ['type', 'value'])

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

    digits = '0123456789'
    is_negative = params.startswith('-')
    params_no_comma = params.replace(',', '').replace('-', '')
    is_number = all([l in digits for l in params_no_comma])
    if is_number:
      value = int(params_no_comma) * (-1 if is_negative else 1)
      return value, 'number'
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

  def parse_modifier(self, raw_modifier: str):
    if not raw_modifier:
      return None
    raw_modifier = raw_modifier.strip()

    if strang_symbols['modifier_not'] == raw_modifier:
      return LexedModifier(type="not", value="not")

    cell_to_int = lambda v: int(v.replace(strang_symbols['cell_prefix'], ''))
    if strang_symbols['cell_prefix'] in raw_modifier:
      cell_chunks = raw_modifier.split(strang_symbols['cell_pointer'])
      from_cell, to_cell = (None, None)
      if len(cell_chunks) == 1:
        from_cell = cell_to_int(cell_chunks[0])
        to_cell = from_cell
      else:
        from_cell = cell_to_int(cell_chunks[0])
        to_cell = cell_to_int(cell_chunks[1])

      cells = (from_cell, to_cell)
      print(cells)
      return LexedModifier(type='cells', value=cells)

    return None

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

    is_null = raw_parent == 'null'
    is_list = not is_str and ',' in raw_parent

    if is_var or is_const:
      title = 'variable' if is_var else 'constant'
      plen = len(strang_symbols[f'{title}_prefix'])
      return LexedParent(type=title, key=raw_parent[plen:])
    elif is_str:
      slen = len(str_start)
      elen = len(str_end) * -1
      return LexedParent(type='string', key=raw_parent[slen:elen])
    elif is_list:
      str_list = raw_parent.replace(' ', '').split(',')
      convert = lambda v: int(v) if not v.startswith(str_start) else str(v[1:-1])
      convert_list = [convert(s) for s in str_list]
      final_list = [s for s in convert_list if not not s]
      return LexedParent(type='list', key=final_list)
    elif is_null:
      return LexedParent(type='null', key=[])
    elif raw_parent == '!strang':
      return LexedParent(type='settings', key='strang')

    return LexedParent(type='node', key='raw_parent')

  def lex_function(self, raw_func):
    func_pattern = r'(.+?)(?: )?([\d|c|!|>]+)?(?: )?(.)>(?: )?(.+)?'
    matches = re.match(func_pattern, raw_func)
    if matches:
      groups = matches.groups()
      c_strip = lambda v: v.strip() if v else None
      func, raw_modifier, key, params = (c_strip(p) for p in groups)

      if key not in self.func_symbols:
        arrow_types = ', '.join([s + '>' for s in self.func_symbols.keys()])
        raise ValueError(f'"{key}>" is not a valid arrow type.\nTry one of the following: "{arrow_types}"')

      func_type = self.func_symbols[key]
      clean_params, param_type = self.parse_params(params)

      modifier = self.parse_modifier(raw_modifier)
      lexed_func = LexedFunction(name=func, ftype=func_type, params=clean_params, ptype=param_type, modifier=modifier)
      return lexed_func

    clean_func = raw_func.strip()

    # Variable
    if clean_func.startswith(strang_symbols['constant_prefix']):
      is_var = clean_func.startswith(strang_symbols['variable_prefix'])
      trim_val = len(strang_symbols['variable_prefix' if is_var else 'constant_prefix'])
      params = clean_func[trim_val:]
      clean_params, ptype = self.parse_params(params)

      fname = 'variable' if is_var else 'constant'
      lexed_func = LexedFunction(name=fname, ftype='map', params=params, ptype=ptype)
      return lexed_func

    # Void Function
    fname = raw_func.strip()
    lexed_func = LexedFunction(name=fname, ftype='map')
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

  def clean_lines(self, raw_code):
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
    return lines_not_empty

  def lex(self, raw_code):
    lines = self.clean_lines(raw_code)

    current_block = 0
    blocks = []
    for line in lines:
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