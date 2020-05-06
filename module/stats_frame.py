from tkinter import *
from wins_breakdown_frame import WinsBreakdownFrame
from match_history_frame import MatchHistoryFrame


class StatsFrame:
    def __init__(self, master, deck):
        self.deck = deck

        self.frame = Frame(master, width=320, height=500, padx=5, pady=5)
        self.deck_name_label = Label(self.frame, text=self.deck.name, bg="black", fg="white", height=3)
        self.wins_breakdown_frame = WinsBreakdownFrame(self.frame, self.deck)
        self.match_history_frame = MatchHistoryFrame(self.frame, self.deck)

        self.adjust_widgets()

    def adjust_widgets(self):
        self.deck_name_label.grid(row=0, column=0, sticky=E+W)

        self.wins_breakdown_frame.frame.grid(row=1, column=0, sticky=E+W, pady=5)

        self.match_history_frame.frame.grid(row=2, column=0, sticky=N+E+W+S, pady=5)

