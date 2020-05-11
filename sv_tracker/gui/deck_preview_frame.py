from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from sv_tracker.class_icons import ClassIcons


class DeckPreviewFrame:
    def __init__(self, master, deck, function):
        self.deck = deck

        self.function = function

        self.class_icon = ClassIcons().get_icon(self.deck.clan())
        self.resized_image = self.class_icon.resize((50, 50))
        self.tk_image = ImageTk.PhotoImage(self.resized_image)

        self.frame = Frame(master, highlightthickness=2)
        self.icon_label = Label(self.frame, image=self.tk_image)
        self.deck_name_label = ttk.Label(self.frame, text=self.deck.name, anchor=W, font="10")
        self.stats_label = self.generate_stats_label(self.frame)

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

    def view_deck(self, event):
        self.function(self.deck)

    def adjust_widgets(self):
        self.icon_label.grid(row=0, column=0, rowspan=2, sticky=N+E+W+S)
        self.deck_name_label.grid(row=0, column=1, sticky=E+W, padx=10)
        self.stats_label.grid(row=1, column=1, sticky=E+W, padx=10)

        self.frame.bind('<Enter>', self.bind_left_click)
        self.frame.bind('<Leave>', self.unbind_left_click)

    def bind_left_click(self, event):
        self.frame.bind_all('<Button-1>', self.view_deck)

    def unbind_left_click(self, event):
        self.frame.unbind_all('<Button-1>')

    def select(self):
        self.frame.config(highlightbackground='blue')

    def deselect(self):
        self.frame.config(highlightbackground=self.frame['bg'])
