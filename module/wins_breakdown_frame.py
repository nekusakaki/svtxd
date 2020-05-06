from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class WinsBreakdownFrame:
    def __init__(self, parent, deck):
        self.deck = deck
        self.wins_breakdown = deck.wins_breakdown()
        self.frame = Frame(parent, width=300, height=225)
        self.wins_chart = self.generate_graph()

    def generate_graph(self):
        if self.wins_breakdown == [0, 0, 0, 0, 0, 0, 0, 0]:
            wins_chart = Label(self.frame, text="NO DATA")
            wins_chart.pack(fill=BOTH, expand=TRUE)
            return wins_chart

        fig = plt.figure(figsize=(4, 3), dpi=75)
        ax = fig.subplots()
        ax.axis('equal')
        classes = ['Forest', 'Sword', 'Rune', 'Dragon', 'Shadow', 'Blood', 'Haven', 'Portal']
        ax.pie(self.wins_breakdown, labels=classes, autopct='%1.2f')
        ax.set_title('Wins Breakdown By Class')

        wins_chart = FigureCanvasTkAgg(fig, self.frame)
        wins_chart.get_tk_widget().pack(fill=BOTH)
        return wins_chart
