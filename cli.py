from strang import Strang

def cli():
  import sys
  args = sys.argv[1:]
  if len(args) == 0:
    print('You must include a strang file!\nUsage: python strang.py example.strang')
    return

  code_filename = args[0]
  html_filename = 'test.html' if len(args) >= 1 else args[1]

  flags = []
  if len(args) > 1:
    flags = [v.replace('-', '') for v in args[1:]]

  if not code_filename.endswith('.strang'):
    code_filename += '.strang'

  with open(f'strang_files/{code_filename}', 'r') as code_file, open(f'html/{html_filename}') as html_file:
    raw_code = code_file.read()
    raw_html = html_file.read()
    functional_context = {}
    strang = Strang(raw_code, raw_html, functional_context, flags)
    strang.execute()