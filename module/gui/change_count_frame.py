from tkinter import *


class ChangeCountFrame:
    def __init__(self, master, card_id, inc_function, dec_function):
        self.card_id = card_id
        self.inc_function = inc_function
        self.dec_function = dec_function

        self.frame = Frame(master)
        self.inc_button = Button(self.frame, text='+', width=3, height=1,
                                 command=self.increment_count, bg='green')
        self.dec_button = Button(self.frame, text='-', width=3, height=1,
                                 command=self.decrement_count, bg='red')

        self.adjust_widgets()

    def increment_count(self):
        self.inc_function(self.card_id)

    def decrement_count(self):
        self.dec_function(self.card_id)

    def resize(self, scale):
        new_width = int(round(4 * scale))
        new_height = int(round(2 * scale))
        self.inc_button.configure(width=new_width, height=new_height)
        self.dec_button.configure(width=new_width, height=new_height)

    def adjust_widgets(self):
        self.inc_button.pack(side=LEFT)
        self.dec_button.pack(side=LEFT)