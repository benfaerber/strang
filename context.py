class Context:
  def __init__(self, first_row: list = []):
    self.container = [first_row]

  def get_cell_count(self):
    return len(self.container)

  def get_column_count(self):
    return len(self.container[0])

  def add_new_cell(self):
    cols = self.get_column_count()
    row = [0 for _ in range(cols)]
    self.container.append(row)

  def get_cell(self, cell_index):
    return self.container[cell_index]

  def set_cell(self, cell_index, new_data):
    cols = self.get_column_count()
    if cols != len(new_data):
      raise ValueError('Cell must be the same length!')

    self.container[cell_index] = new_data

  def swap_cells(self, swap_this, swap_that):
    this_cell = self.container[swap_this]
    that_cell = self.container[swap_that]

    self.container[swap_this] = that_cell
    self.container[swap_that] = this_cell