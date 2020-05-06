from tkinter import *


class DeckPreviewFrame:
    def __init__(self, master, deck, function):
        self.deck = deck

        self.function = function

        self.frame = Frame(master, bd=0)
        self.icon_canvas = Canvas(self.frame, width=100, height=100)
        self.deck_name_label = Label(self.frame, text=self.deck.name, anchor=W)
        self.stats_label = self.generate_stats_label(self.frame)
        self.view_button = Button(self.frame, text='VIEW', command=self.view_deck)

        self.fill_icon_canvas()
        self.adjust_widgets()

    def generate_stats_label(self, master):
        text = ""
        if self.deck.wins() + self.deck.losses() == 0:
            text = "No Stats"
        else:
            win_rate = '{:.2f}'.format(self.deck.win_rate())
            text = win_rate + ' | ' + str(self.deck.wins()) + '-' + str(self.deck.losses())
        label = Label(master, text=text, anchor=W)
        return label

    def view_deck(self):
        self.function(self.deck)

    def fill_icon_canvas(self):
        self.icon_canvas.create_text((50, 50), text=self.deck.clan(), anchor=CENTER)

    def adjust_widgets(self):
        self.icon_canvas.grid(row=0, column=0, rowspan=2, sticky=N+E+W+S)
        self.deck_name_label.grid(row=0, column=1, sticky=E+W)
        self.stats_label.grid(row=1, column=1, sticky=E+W)
        self.view_button.grid(row=0, column=2, rowspan=2, sticky=E+W)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=3)
        self.frame.columnconfigure(2, weight=1)