from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sv_tracker.helper_functions as hf


class LossesBreakdownFrame(Frame):
    def __init__(self, master, deck):
        self.deck = deck
        self.losses_breakdown = deck.losses_breakdown()
        super().__init__(master, width=300, height=225)
        self.losses_chart = self.generate_graph()

    def generate_graph(self):
        if self.losses_breakdown == [0, 0, 0, 0, 0, 0, 0, 0]:
            losses_chart = Label(self, text="NO DATA", font='Times 36 bold')
            losses_chart.pack(fill=BOTH, expand=TRUE)
            return losses_chart

        fig = plt.figure(figsize=(4, 3), dpi=75)
        ax = fig.subplots()
        ax.axis('equal')
        classes = ['Forest', 'Sword', 'Rune', 'Dragon', 'Shadow', 'Blood', 'Haven', 'Portal']
        colors = ['#339900', '#D7CD4C', '#333399', '#CC6633', '#9D87DE', '#990033', '#B0A979', '#41ACE1']
        total = sum(self.losses_breakdown)
        ax.pie(self.losses_breakdown, labels=classes, colors=colors,
               autopct=lambda p: '{:.0f}'.format(p * total / 100))
        ax.set_title('Losses Breakdown By Class')

        background = hf.rgb_to_hex(self.winfo_rgb(self['bg']))
        fig.patch.set_facecolor(background)

        losses_chart = FigureCanvasTkAgg(fig, self)
        losses_chart.get_tk_widget().pack(fill=BOTH)
        return losses_chart

    def destroy(self):
        if type(self.losses_chart) is Label:
            super().destroy()
            return

        plt.close(self.losses_chart.figure)
        super().destroy()
