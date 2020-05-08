from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sv_tracker.helper_functions as hf


class FirstBreakdownFrame:
    def __init__(self, parent, deck):
        self.deck = deck
        self.first_breakdown = deck.first_breakdown()
        self.frame = Frame(parent, width=300, height=225)
        self.first_chart = self.generate_graph()

    def generate_graph(self):
        if self.first_breakdown == [0, 0]:
            first_chart = Label(self.frame, text="NO DATA", font='Times 36 bold')
            first_chart.pack(fill=BOTH, expand=TRUE)
            return first_chart

        fig = plt.figure(figsize=(4, 3), dpi=75)
        ax = fig.subplots()
        ax.axis('equal')
        legend = ['Wins', 'Losses']
        ax.pie(self.first_breakdown, labels=legend, autopct='%1.2f')
        ax.set_title('Going First Breakdown')

        background = hf.rgb_to_hex(self.frame.winfo_rgb(self.frame['bg']))
        fig.patch.set_facecolor(background)

        first_chart = FigureCanvasTkAgg(fig, self.frame)
        first_chart.get_tk_widget().pack(fill=BOTH)
        return first_chart
