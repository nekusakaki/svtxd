from tkinter import *
from PIL import Image, ImageTk


class ChangeCountFrame(Frame):
    def __init__(self, master, card_id, inc_function, dec_function):
        self.card_id = card_id
        self.inc_function = inc_function
        self.dec_function = dec_function

        super().__init__(master)

        self.plus_img = Image.open('images/plus.png')
        self.resized_plus = self.plus_img.resize((50, 50))
        self.tk_plus = ImageTk.PhotoImage(self.resized_plus)
        self.inc_button = Button(self, image=self.tk_plus, borderwidth=0,
                                 command=self.increment_count)

        self.minus_img = Image.open('images/minus.png')
        self.resized_minus = self.minus_img.resize((50, 50))
        self.tk_minus = ImageTk.PhotoImage(self.resized_minus)
        self.dec_button = Button(self, image=self.tk_minus, borderwidth=0,
                                 command=self.decrement_count)

        self.adjust_widgets()

    def increment_count(self):
        self.inc_function(self.card_id)

    def decrement_count(self):
        self.dec_function(self.card_id)

    def resize(self, scale):
        new_width = int(round(41 * scale))
        new_height = int(round(41 * scale))

        self.resized_plus = self.plus_img.resize((new_width, new_height))
        self.tk_plus = ImageTk.PhotoImage(self.resized_plus)
        self.inc_button.configure(image=self.tk_plus, width=new_width, height=new_height)

        self.resized_minus = self.minus_img.resize((new_width, new_height))
        self.tk_minus = ImageTk.PhotoImage(self.resized_minus)
        self.dec_button.configure(image=self.tk_minus, width=new_width, height=new_height)

    def adjust_widgets(self):
        self.inc_button.pack(side=LEFT)
        self.dec_button.pack(side=LEFT, padx=3)
