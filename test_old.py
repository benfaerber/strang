from strang import Strang

# out log
def double(context, params=None):
  return context * 2

#  ;filter -> $ '.js' => in


def load_test():
  with open('./wiki.html', 'r') as file:
    return file.read()

def load_strang_code():
  with open('./test.strang', 'r') as file:
    return file.read()

def main():
  function_context = {
    'double': double
  }

  strang_code = load_strang_code()
  raw_html = load_test()
  strang = Strang(strang_code, raw_html, function_context)
  strang.start()

if __name__ == '__main__':
  main()