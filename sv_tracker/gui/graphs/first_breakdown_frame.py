from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sv_tracker.helper_functions as hf


class FirstBreakdownFrame(Frame):
    def __init__(self, master, deck):
        self.deck = deck
        self.first_breakdown = deck.first_breakdown()
        super().__init__(master, width=300, height=225)
        self.first_chart = self.generate_graph()

    def generate_graph(self):
        if self.first_breakdown == [0, 0]:
            first_chart = Label(self, text="NO DATA", font='Times 36 bold')
            first_chart.pack(fill=BOTH, expand=TRUE)
            return first_chart

        fig = plt.figure(figsize=(4, 3), dpi=75)
        ax = fig.subplots()
        ax.axis('equal')
        legend = ['Wins', 'Losses']
        colors = ['#339900', '#990033']
        ax.pie(self.first_breakdown, labels=legend, colors=colors, autopct='%1.2f')
        ax.set_title('Going First Breakdown')

        background = hf.rgb_to_hex(self.winfo_rgb(self['bg']))
        fig.patch.set_facecolor(background)

        first_chart = FigureCanvasTkAgg(fig, self)
        first_chart.get_tk_widget().pack(fill=BOTH)
        return first_chart

    def destroy(self):
        if type(self.first_chart) is Label:
            super().destroy()
            return

        plt.close(self.first_chart.figure)
        super().destroy()
