from strang import Strang

def run_tests():
  functional_context = {}

  with open('strang_files/test.strang', 'r') as code_file, open('html/test.html', 'r') as html_file:
    raw_code = code_file.read()
    raw_html = html_file.read()
    strang = Strang(raw_code, raw_html, functional_context)
    strang.execute()

def main():
  run_tests()

if __name__ == '__main__':
    main()