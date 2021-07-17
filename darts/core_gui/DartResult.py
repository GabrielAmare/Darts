from tkinter import *

from darts.app_data import app_data
from darts.base_gui import ButtonWrap

VALUES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25]
FACTORS = [1, 2, 3]


class DartResult(Frame):
    """This displays a grid where all the target areas are represented."""

    def __init__(self, root, **cfg):
        super().__init__(root, **cfg)

        self.values = ButtonWrap(self, wrap_width=11, grid_config=dict(padx=1, pady=1), style='DartResult.button')
        for value in VALUES:
            text = 'BULL' if value == 25 else str(value)
            self.values.new_button(key=str(value), text=text)

        self.factors = ButtonWrap(self, wrap_width=1, grid_config=dict(padx=1, pady=1), style='DartResult.button')
        for factor in FACTORS:
            button = self.factors.new_button(key=str(factor), text=str(factor))
            button.disable()

        self.values.set('0')
        self.factors.set('')

        app_data.styles.config(self, 'DartResult')
        app_data.styles.config(self.values, 'DartResult.values')
        app_data.styles.config(self.factors, 'DartResult.factors')

        self.values.pack(side=LEFT, padx=8)
        self.factors.pack(side=LEFT, padx=8)

        self.values.selector.on('set', self.on_set_value)

    def on_set_value(self, key: str):
        if key == '0':
            self.factors.disable('1')
            self.factors.disable('2')
            self.factors.disable('3')
            self.factors.set('')
        elif key == '25':
            self.factors.enable('1')
            self.factors.enable('2')
            self.factors.disable('3')
            if self.factors.get() == '3':
                self.factors.set('')
        else:
            self.factors.enable('1')
            self.factors.enable('2')
            self.factors.enable('3')

        # app_data.styles.config(self, 'default')
        # factor_keys = {1: 'SIMPLE', 2: 'DOUBLE', 3: 'TRIPLE'}
        # listeOptions = list(factor_keys.values())
        # v = IntVar(self)
        # v.set(listeOptions[0])
        # om = OptionMenu(self, v, *listeOptions)
        # om.pack(side=LEFT, fill=Y)
        # app_data.styles.config(om, 'DartResult.button')
        #
        # listeOptions = VALUES
        # v = IntVar(self)
        # v.set(listeOptions[0])
        # om2 = OptionMenu(self, v, *listeOptions)
        # om2.pack(side=LEFT, fill=Y)
        # app_data.styles.config(om2, 'DartResult.button')

        # for row, factor in enumerate(FACTORS):
        #     factor_key = {1: 'SIMPLE', 2: 'DOUBLE', 3: 'TRIPLE'}[factor]
        #     button = Button(self, code=f"APP.FACTORS.{factor_key}")
        #     app_data.styles.config(button, 'DartResult.button')
        #     button.grid(row=row, column=0, sticky=NSEW)
        #
        #     self.grid_rowconfigure(row, weight=1)
        #
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)
        #
        # for column in range(7):
        #     for row in range(3):
        #         index = row + 3 * column
        #         value = VALUES[index]
        #
        #         button = Button(self, text=str(value))
        #         app_data.styles.config(button, 'DartResult.button')
        #         button.grid(row=row, column=column + 2, sticky=NSEW)
        #
        #     self.grid_columnconfigure(column + 2, weight=1)
        #
        # self.grid_columnconfigure(9, weight=1)
        #
        # end = Button(self, text='->')
        # app_data.styles.config(end, 'DartResult.button')
        # end.grid(row=1, column=10, sticky=NSEW)
        #
        # self.grid_columnconfigure(10, weight=1)
