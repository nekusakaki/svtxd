from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from class_icons import ClassIcons


class DeckPreviewFrame:
    def __init__(self, master, deck, function):
        self.deck = deck

        self.function = function

        self.class_icon = ClassIcons().get_icon(self.deck.clan())
        self.tk_image = ImageTk.PhotoImage(self.class_icon)

        self.frame = ttk.Frame(master)
        self.icon_label = Label(self.frame, image=self.tk_image)
        self.deck_name_label = ttk.Label(self.frame, text=self.deck.name, width=22, anchor=W, font="8")
        self.stats_label = self.generate_stats_label(self.frame)
        self.view_button = ttk.Button(self.frame, text='VIEW', command=self.view_deck)

        self.adjust_widgets()

    def generate_stats_label(self, master):
        text = ""
        if self.deck.wins() + self.deck.losses() == 0:
            text = "No Stats"
        else:
            win_rate = '{:.2f}'.format(self.deck.win_rate())
            text = win_rate + ' | ' + str(self.deck.wins()) + '-' + str(self.deck.losses())
        label = ttk.Label(master, text=text, anchor=W)
        return label

    def view_deck(self):
        self.function(self.deck)

    def adjust_widgets(self):
        self.icon_label.grid(row=0, column=0, rowspan=2, sticky=N+E+W+S)
        self.deck_name_label.grid(row=0, column=1, sticky=E+W)
        self.stats_label.grid(row=1, column=1, sticky=E+W)
        self.view_button.grid(row=0, column=2, rowspan=2, sticky=E+W)
