from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sv_tracker.helper_functions as hf


class WinsBreakdownFrame:
    def __init__(self, parent, deck):
        self.deck = deck
        self.wins_breakdown = deck.wins_breakdown()
        self.frame = Frame(parent, width=300, height=225)
        self.wins_chart = self.generate_graph()

    def generate_graph(self):
        if self.wins_breakdown == [0, 0, 0, 0, 0, 0, 0, 0]:
            wins_chart = Label(self.frame, text="NO DATA", font='Times 36 bold')
            wins_chart.pack(fill=BOTH, expand=TRUE)
            return wins_chart

        fig = plt.figure(figsize=(4, 3), dpi=75)
        ax = fig.subplots()
        ax.axis('equal')
        classes = ['Forest', 'Sword', 'Rune', 'Dragon', 'Shadow', 'Blood', 'Haven', 'Portal']
        total = sum(self.wins_breakdown)
        ax.pie(self.wins_breakdown, labels=classes, autopct=lambda p: '{:.0f}'.format(p * total / 100))
        ax.set_title('Wins Breakdown By Class')

        background = hf.rgb_to_hex(self.frame.winfo_rgb(self.frame['bg']))
        fig.patch.set_facecolor(background)

        wins_chart = FigureCanvasTkAgg(fig, self.frame)
        wins_chart.get_tk_widget().pack(fill=BOTH)
        return wins_chart

    def destroy(self):
        if type(self.wins_chart) is Label:
            return

        plt.close(self.wins_chart.figure)
