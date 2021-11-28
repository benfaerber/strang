
def get_attr(attr, c):
  attr_table = {
    'text': lambda k: k.text,
    'html': lambda k: k.html,
    'src': lambda k: k.src
  }

  if attr in attr_table:
    return attr_table[attr](c)

  return c.get(attr)