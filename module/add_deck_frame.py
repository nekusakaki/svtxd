from tkinter import *
from tkinter import messagebox
from deck import Deck


class AddDeckFrame:
    def __init__(self, master, function):
        self.add_deck_function = function

        self.frame = Frame(master)
        self.deck_name_label = Label(self.frame, text="Deck Name: ")
        self.deck_name_entry = Entry(self.frame, width=30)
        self.deck_code_label = Label(self.frame, text="Deck Code: ")
        self.deck_code_entry = Entry(self.frame, width=5)
        self.enter_button = Button(self.frame, text='Enter', command=self.add_deck)

        self.adjust_widgets()

    def add_deck(self):
        deck_name = self.deck_name_entry.get()
        deck_code = self.deck_code_entry.get()

        if not deck_name:
            messagebox.showinfo("Error", "Invalid deck name.")
            return

        if not len(deck_code) == 4:
            messagebox.showinfo("Error", "Invalid deck code.")
            return

        deck = Deck.generate_from_deck_code(deck_name, deck_code)
        if not deck:
            messagebox.showinfo("Error", "Invalid or expired deck code.")
            return

        self.add_deck_function(deck)

    def adjust_widgets(self):
        self.deck_name_label.grid(row=0, column=0)

        self.deck_name_entry.grid(row=0, column=1)

        self.deck_code_label.grid(row=1, column=0)

        self.deck_code_entry.grid(row=1, column=1)

        self.enter_button.grid(row=2, column=0, columnspan=2)
