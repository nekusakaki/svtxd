from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from sv_tracker.deck import Deck


class AddDeckFrame(Frame):
    def __init__(self, master, function):
        self.add_deck_function = function

        super().__init__(master)
        self.deck_name_label = ttk.Label(self, text="Deck Name: ")
        self.deck_name_entry = ttk.Entry(self, width=30)
        self.deck_code_label = ttk.Label(self, text="Deck Code: ")
        self.deck_code_entry = ttk.Entry(self, width=5)
        self.enter_button = ttk.Button(self, text='Enter', command=self.add_deck)

        self.adjust_widgets()

    def add_deck(self):
        deck_name = self.deck_name_entry.get()
        deck_code = self.deck_code_entry.get()

        if not deck_name:
            messagebox.showinfo("Error", "Invalid deck name.")
            self.return_focus()
            return

        if not len(deck_code) == 4:
            messagebox.showinfo("Error", "Invalid deck code.")
            self.return_focus()
            return

        try:
            deck = Deck.generate_from_deck_code(deck_name, deck_code)
        except ValueError:
            messagebox.showinfo("Error", "Invalid or expired deck code.")
            self.return_focus()
            return
        else:
            self.add_deck_function(deck)

    def return_focus(self):
        self.master.lift()
        self.master.focus_force()

    def adjust_widgets(self):
        self.deck_name_label.grid(row=0, column=0)

        self.deck_name_entry.grid(row=0, column=1)

        self.deck_code_label.grid(row=1, column=0)

        self.deck_code_entry.grid(row=1, column=1)

        self.enter_button.grid(row=2, column=0, columnspan=2)

        self.bind('<FocusIn>', self.handle_focus)
        self.bind('<FocusOut>', self.handle_unfocus)

    def handle_focus(self, event):
        self.bind_all('<Return>', self.enter_pressed)

    def enter_pressed(self, event):
        self.add_deck()

    def handle_unfocus(self, event):
        self.unbind_all('<Return>')
