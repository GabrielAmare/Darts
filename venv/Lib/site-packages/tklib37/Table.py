from tkinter import Frame, NSEW


class Table(Frame):
    def __init__(self, root, **cfg):
        super().__init__(root, **cfg)
        self.widgets = {}
        self.row_weights, self.col_weights = {}, {}

    @property
    def n_cols(self):
        return max((col for row, col in self.widgets.keys()), default=-1) + 1

    @property
    def n_rows(self):
        return max((row for row, col in self.widgets.keys()), default=-1) + 1

    def _set_widget(self, row: int, col: int, cls, **cfg):
        widget = cls(self, **cfg)
        self._put_widget(row, col, widget)

        if row not in self.row_weights:
            self.row_weights[row] = 1
            self.rowconfigure(row, weight=1)

        if col not in self.col_weights:
            self.col_weights[col] = 1
            self.columnconfigure(col, weight=1)

        return widget

    def _upd_widget(self, row: int, col: int, **cfg):
        widget = self._get_widget(row, col)
        if widget:
            widget.configure(**cfg)

    def _get_widget(self, row: int, col: int):
        return self.widgets.get((row, col), None)

    def _del_widget(self, row: int, col: int):
        widget = self._pop_widget(row, col)
        if widget:
            widget.destroy()

    def _pop_widget(self, row: int, col: int):
        if (row, col) in self.widgets:
            widget = self.widgets.pop((row, col))
            widget.grid_forget()
            return widget

    def _put_widget(self, row: int, col: int, widget):
        if widget:
            self.widgets[(row, col)] = widget
            widget.grid(row=row, column=col, sticky=NSEW)

    def _invert_widgets(self, old_row: int, old_col: int, new_row: int, new_col: int):
        old_widget = self._pop_widget(old_row, old_col)
        new_widget = self._pop_widget(new_row, new_col)

        self._put_widget(old_row, old_col, new_widget)
        self._put_widget(new_row, new_col, old_widget)

    def _invert_rows(self, old_row: int, new_row: int):
        for col in range(self.n_cols):
            self._invert_widgets(old_row, col, new_row, col)

        self.row_weights[old_row], self.row_weights[new_row] = self.row_weights.get(new_row, 1), self.row_weights.get(old_row, 1)
        self.rowconfigure(old_row, weight=self.row_weights[old_row])
        self.rowconfigure(new_row, weight=self.row_weights[new_row])

    def _invert_cols(self, old_col: int, new_col: int):
        for row in range(self.n_rows):
            self._invert_widgets(row, old_col, row, new_col)

        self.col_weights[old_col], self.col_weights[new_col] = self.col_weights.get(new_col, 1), self.col_weights.get(old_col, 1)
        self.columnconfigure(old_col, weight=self.col_weights[old_col])
        self.columnconfigure(new_col, weight=self.col_weights[new_col])

    def _del_row(self, row: int):
        to_del = [col for row_, col in self.widgets if row_ == row]

        for col in to_del:
            self.del_widget(row, col)

        if row in self.row_weights:
            del self.row_weights[row]
        self.rowconfigure(row, weight=0)

    def _del_col(self, col: int):
        to_del = [row for row, col_ in self.widgets if col_ == col]

        for row in to_del:
            self.del_widget(row, col)

        if col in self.col_weights:
            del self.col_weights[col]
        self.columnconfigure(col, weight=0)

    def set_widget(self, row, col, cls, **cfg):
        """Set a widget at a row & column"""
        return self._set_widget(row, col, cls, **cfg)

    def upd_widget(self, row, col, **cfg):
        """Get a widget by it's row & column"""
        return self._upd_widget(row, col, **cfg)

    def get_widget(self, row: int, col: int):
        """Update a widget config"""
        return self._get_widget(row, col)

    def del_widget(self, row: int, col: int):
        """Delete a widget"""
        return self._del_widget(row, col)

    def invert_widgets(self, old_row: int, old_col: int, new_row: int, new_col: int):
        """Invert two widgets"""
        return self._invert_widgets(old_row, old_col, new_row, new_col)

    def invert_rows(self, old_row: int, new_row: int):
        """Invert two rows"""
        return self._invert_rows(old_row, new_row)

    def invert_cols(self, old_col: int, new_col: int):
        """Invert two columns"""
        return self._invert_cols(old_col, new_col)

    def del_row(self, row: int):
        """Delete a row"""
        self._del_row(row)

    def del_col(self, col: int):
        """Delete a column"""
        self._del_col(col)
