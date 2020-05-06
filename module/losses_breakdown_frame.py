from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class LossesBreakdownFrame:
    def __init__(self, parent, deck):
        self.deck = deck
        self.losses_breakdown = deck.losses_breakdown()
        self.frame = Frame(parent, width=300, height=225)
        self.losses_chart = self.generate_graph()

    def generate_graph(self):
        if self.losses_breakdown == [0, 0, 0, 0, 0, 0, 0, 0]:
            losses_chart = Label(self.frame, text="NO DATA")
            losses_chart.pack(fill=BOTH, expand=TRUE)
            return losses_chart

        fig = plt.figure(figsize=(4, 3), dpi=75)
        ax = fig.subplots()
        ax.axis('equal')
        classes = ['Forest', 'Sword', 'Rune', 'Dragon', 'Shadow', 'Blood', 'Haven', 'Portal']
        ax.pie(self.losses_breakdown, labels=classes, autopct='%1.2f')
        ax.set_title('Losses Breakdown By Class')

        losses_chart = FigureCanvasTkAgg(fig, self.frame)
        losses_chart.get_tk_widget().pack(fill=BOTH)
        return losses_chart
