from pathlib import Path
from datetime import datetime

class TableLogger:
  def __init__(self, col_labels, log_dir=None, col_types=None, col_lengths=None, do_print=False, eol="\n"):
    if log_dir is not None:
      self.log_dir = Path(log_dir)
      now = datetime.now()
      self.file_path = self.log_dir / f"{now.date()}_{now.hour}_{now.minute}.log"
    else:
      self.file_path = None
    self.do_print = do_print
    self.n_cols = len(col_labels)
    self.eol = eol
    if col_types is None:
      col_types = [str for i in range(self.n_cols)]
    
    if col_lengths is None:
      # col_lengths = [15 for i in range(self.n_cols)]
      col_lengths = [max(3, len(label)) for label in col_labels]
    assert len(col_labels) == len(col_types) == len(col_lengths)

    self.col_labels = col_labels
    self.col_types = col_types
    self.col_lengths = col_lengths
    self.format_str = [f"{{:<{col_lengths[i]}.{col_lengths[i]}}}" for i in range(self.n_cols)]
    self.format_str = f"| {' | '.join(self.format_str)} |{self.eol}"
    # self.title_line = self.format_str.format(*self.col_labels)
    # self.dash_line = self.format_str.format(*["-"*i for i in self.col_lengths])

    self.title_line = self.add_row(self.col_labels, remember_types=False)
    self.dash_line = self.add_row(["-"*i for i in self.col_lengths], remember_types=False)

  def add_row(self, row_items, remember_types=True):
    assert len(row_items) == self.n_cols
    if remember_types:
      self.col_types = [type(item) for item in row_items]
    line = self.format_str.format(*[str(item) for item in row_items])
    if self.file_path is not None:
      with open(self.file_path, "a") as f:
        f.write(line)
    if self.do_print:
      print(line)
    return line

  def read_row(self, row):
    items = row.split("|")[1:-1]
    if len(items) != self.n_cols:
      return None
    
    # items = [item.strip() for item in items]
    items = [items[i].strip() for i in range(self.n_cols)]
    items = [self.col_types[i](items[i]) for i in range(self.n_cols)]
    return items

  def read_table(self):
    if self.file_path is not None:
      with open(self.file_path, "r") as f:
        rows = f.read().split(self.eol)[2:]
      row_items = [self.read_row(row) for row in rows]
      row_items = [i for i in row_items if i is not None]
      return row_items
    else:
      return []