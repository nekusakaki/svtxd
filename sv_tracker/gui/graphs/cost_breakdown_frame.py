from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sv_tracker.helper_functions as hf


class CostBreakdownFrame(Frame):
    def __init__(self, master, deck):
        self.cost_breakdown = deck.cost_breakdown()
        super().__init__(master, width=150, height=150)
        self.cost_chart = self.generate_graph()

    def generate_graph(self):
        follower_counts = []
        amulet_counts = []
        spell_counts = []

        for index, cost in enumerate(self.cost_breakdown):
            follower_count = self.cost_breakdown[cost][0]
            amulet_count = self.cost_breakdown[cost][1]
            spell_count = self.cost_breakdown[cost][2]

            follower_counts.append(follower_count)
            amulet_counts.append(amulet_count)
            spell_counts.append(spell_count)

        fa_counts = [x + y for x, y in zip(follower_counts, amulet_counts)]
        labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8+']
        width = 0.9
        fig = plt.Figure(figsize=(2, 2), dpi=75)
        ax = fig.subplots()
        ax.bar(labels, follower_counts, width, color='#333399', label='Followers')
        ax.bar(labels, amulet_counts, width, bottom=follower_counts, color='#339900', label='Amulets')
        ax.bar(labels, spell_counts, width, bottom=fa_counts, color='#990033', label='Spells')
        ax.yaxis.set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)
        background_color = hf.rgb_to_hex(self.winfo_rgb(self['bg']))
        fig.legend()
        ax.set_facecolor(background_color)
        ax.set_title('Cost Breakdown')

        fig.patch.set_facecolor(background_color)

        cost_chart = FigureCanvasTkAgg(fig, self)
        cost_chart.get_tk_widget().pack(fill=BOTH)
        return cost_chart

    def resize(self, event):
        self.configure(width=event.width, height=event.width)

    def destroy(self):
        plt.close(self.cost_chart.figure)
        super().destroy()
