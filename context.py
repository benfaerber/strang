class Context:
  def __init__(self, context: list = [], complete: bool = False):
    self._container = [context] if not complete else context

  def get_cell_count(self):
    return len(self._container)

  def get_column_count(self):
    return len(self._container[0])

  def add_new_cell(self):
    cols = self.get_column_count()
    row = [0 for _ in range(cols)]
    self._container.append(row)

  def should_add(self, cell_index):
    if len(self._container) < cell_index:
      self.add_new_cell()

  def get_cell(self, cell_index):
    self.should_add(cell_index)
    return self._container[cell_index - 1]

  def get_cell_type(self, cell_index):
    type_names = {
      int: 'int',
      str: 'str',
      list: 'list',
      bool: 'bool',
      float: 'float'
    }

    cell = self.get_cell(cell_index)
    if cell and len(cell) != 0:
      first_type = type(cell[0])
      return type_names[first_type]
    return 'int'

  def set_cell(self, cell_index, new_data):
    self.should_add(cell_index)
    self._container[cell_index - 1] = new_data

  def swap_cells(self, swap_this, swap_that):
    this_cell = self._container[swap_this]
    that_cell = self._container[swap_that]

    self._container[swap_this] = that_cell
    self._container[swap_that] = this_cell

  def get_data(self):
    return self._container

  def __repr__(self):
    return f'Context({self._container})'
