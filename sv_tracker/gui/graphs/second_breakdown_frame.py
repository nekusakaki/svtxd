from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sv_tracker.helper_functions as hf


class SecondBreakdownFrame(Frame):
    def __init__(self, master, deck):
        self.deck = deck
        self.second_breakdown = deck.second_breakdown()
        super().__init__(master, width=300, height=225)
        self.second_chart = self.generate_graph()

    def generate_graph(self):
        if self.second_breakdown == [0, 0]:
            second_chart = Label(self, text="NO DATA", font='Times 36 bold')
            second_chart.pack(fill=BOTH, expand=TRUE)
            return second_chart

        fig = plt.figure(figsize=(4, 3), dpi=75)
        ax = fig.subplots()
        ax.axis('equal')
        legend = ['Wins', 'Losses']
        colors = ['#339900', '#990033']
        ax.pie(self.second_breakdown, labels=legend, colors=colors, autopct='%1.2f')
        ax.set_title('Going Second Breakdown')

        background = hf.rgb_to_hex(self.winfo_rgb(self['bg']))
        fig.patch.set_facecolor(background)

        second_chart = FigureCanvasTkAgg(fig, self)
        second_chart.get_tk_widget().pack(fill=BOTH)
        return second_chart

    def destroy(self):
        if type(self.second_chart) is Label:
            super().destroy()
            return

        super().destroy()
        plt.close(self.second_chart.figure)
