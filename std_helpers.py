
def destruct(data, c=3):
  if c == 1:
    return data['context']
  elif c == 2:
    return (data['context'] or None, data['params'] or None)

  return (data['context'] or None, data['params'] or None, data['ptype'] or None)


def get_attr(attr, c):
  attr_table = {
    'text': lambda k: k.text,
    'html': lambda k: k.html,
    'src': lambda k: k.src
  }

  if attr in attr_table:
    return attr_table[attr](c)

  return c.get(attr)