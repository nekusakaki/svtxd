from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SecondBreakdownFrame:
    def __init__(self, parent, deck):
        self.deck = deck
        self.second_breakdown = deck.second_breakdown()
        self.frame = Frame(parent, width=300, height=225)
        self.second_chart = self.generate_graph()

    def generate_graph(self):
        if self.second_breakdown == [0, 0]:
            second_chart = Label(self.frame, text="NO DATA")
            second_chart.pack(fill=BOTH, expand=TRUE)
            return second_chart

        fig = plt.figure(figsize=(4, 3), dpi=75)
        ax = fig.subplots()
        ax.axis('equal')
        legend = ['Wins', 'Losses']
        ax.pie(self.second_breakdown, labels=legend, autopct='%1.2f')
        ax.set_title('Going Second Breakdown')

        second_chart = FigureCanvasTkAgg(fig, self.frame)
        second_chart.get_tk_widget().pack(fill=BOTH)
        return second_chart
