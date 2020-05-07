from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import helper_functions as hf


class MatchBreakdownFrame:
    def __init__(self, parent, deck):
        self.deck = deck
        wins = self.deck.wins_breakdown()
        losses = self.deck.losses_breakdown()
        self.match_breakdown = [x + y for x, y in zip(wins, losses)]
        self.frame = Frame(parent, width=300, height=225)
        self.match_chart = self.generate_graph()

    def generate_graph(self):
        if self.match_breakdown == [0, 0, 0, 0, 0, 0, 0, 0]:
            match_chart = Label(self.frame, text="NO DATA", font='Times 36 bold')
            match_chart.pack(fill=BOTH, expand=TRUE)
            return match_chart

        fig = plt.figure(figsize=(4, 3), dpi=75)
        ax = fig.subplots()
        ax.axis('equal')
        classes = ['Forest', 'Sword', 'Rune', 'Dragon', 'Shadow', 'Blood', 'Haven', 'Portal']
        ax.pie(self.match_breakdown, labels=classes, autopct='%1.2f')

        ax.set_title('Opponent Breakdown By Class')

        background = hf.rgb_to_hex(self.frame.winfo_rgb(self.frame['bg']))
        fig.patch.set_facecolor(background)

        match_chart = FigureCanvasTkAgg(fig, self.frame)
        match_chart.get_tk_widget().pack(fill=BOTH)
        return match_chart
