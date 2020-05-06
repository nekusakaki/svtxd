from tkinter import *
from tkinter import ttk
from wins_breakdown_frame import WinsBreakdownFrame
from match_history_frame import MatchHistoryFrame
from losses_breakdown_frame import LossesBreakdownFrame
from first_breakdown_frame import FirstBreakdownFrame
from second_breakdown_frame import SecondBreakdownFrame


class StatsFrame:
    def __init__(self, master, deck):
        self.deck = deck

        self.frame = Frame(master, width=320, height=500, padx=5, pady=5)
        self.deck_name_label = Label(self.frame, text=self.deck.name, bg="black", fg="white", height=3)

        self.figures_notebook = ttk.Notebook(self.frame)
        self.wins_breakdown_frame = WinsBreakdownFrame(self.figures_notebook, self.deck)
        self.losses_breakdown_frame = LossesBreakdownFrame(self.figures_notebook, self.deck)
        self.first_breakdown_frame = FirstBreakdownFrame(self.figures_notebook, self.deck)
        self.second_breakdown_frame = SecondBreakdownFrame(self.figures_notebook, self.deck)

        self.match_history_frame = MatchHistoryFrame(self.frame, self.deck)

        self.adjust_widgets()

    def adjust_widgets(self):
        self.deck_name_label.grid(row=0, column=0, sticky=E+W)

        self.wins_breakdown_frame.frame.pack(fill=BOTH, expand=True)
        self.losses_breakdown_frame.frame.pack(fill=BOTH, expand=True)
        self.first_breakdown_frame.frame.pack(fill=BOTH, expand=True)
        self.second_breakdown_frame.frame.pack(fill=BOTH, expand=True)

        self.match_history_frame.frame.grid(row=2, column=0, sticky=N+E+W+S, pady=5)

        self.figures_notebook.grid(row=1, column=0, sticky=E+W, pady=5)
        self.figures_notebook.add(self.wins_breakdown_frame.frame, text='Wins')
        self.figures_notebook.add(self.losses_breakdown_frame.frame, text='Losses')
        self.figures_notebook.add(self.first_breakdown_frame.frame, text='First')
        self.figures_notebook.add(self.second_breakdown_frame.frame, text='Second')

