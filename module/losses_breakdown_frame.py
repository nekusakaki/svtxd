from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import helper_functions as hf


class LossesBreakdownFrame:
    def __init__(self, parent, deck):
        self.deck = deck
        self.losses_breakdown = deck.losses_breakdown()
        self.frame = Frame(parent, width=300, height=225)
        self.losses_chart = self.generate_graph()

    def generate_graph(self):
        if self.losses_breakdown == [0, 0, 0, 0, 0, 0, 0, 0]:
            losses_chart = Label(self.frame, text="NO DATA", font='Times 36 bold')
            losses_chart.pack(fill=BOTH, expand=TRUE)
            return losses_chart

        fig = plt.figure(figsize=(4, 3), dpi=75)
        ax = fig.subplots()
        ax.axis('equal')
        classes = ['Forest', 'Sword', 'Rune', 'Dragon', 'Shadow', 'Blood', 'Haven', 'Portal']
        total = sum(self.losses_breakdown)
        ax.pie(self.losses_breakdown, labels=classes, autopct=lambda p: '{:.0f}'.format(p * total / 100))
        ax.set_title('Losses Breakdown By Class')

        background = hf.rgb_to_hex(self.frame.winfo_rgb(self.frame['bg']))
        fig.patch.set_facecolor(background)

        losses_chart = FigureCanvasTkAgg(fig, self.frame)
        losses_chart.get_tk_widget().pack(fill=BOTH)
        return losses_chart
