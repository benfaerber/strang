from collections import namedtuple
from context import Context

class FunctionCall:
  def __init__(self, function, lexed_function: namedtuple, context: Context, acc=None, flags=[]):
    self.function = function

    self.params = lexed_function.params
    self.ptype = lexed_function.ptype
    self.modifier = lexed_function.modifier if lexed_function.modifier else None

    self.cells = (1, 1)
    if self.modifier and self.modifier.type == 'cells':
      self.cells = self.modifier.value

    self.context = context
    self.acc = acc
    self.flags = flags

  def __repr__(self):
    return f'FunctionCall(function={self.function}, params=\'{self.params}\', ptype=\'{self.ptype}\', context={self.context}, modifier={self.modifier}, cells={self.cells})'
