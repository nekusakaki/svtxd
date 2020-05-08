from tkinter import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sv_tracker.helper_functions as hf


class CostBreakdownFrame:
    def __init__(self, parent, decklist):
        self.cost_breakdown = decklist.cost_breakdown()
        self.frame = Frame(parent, width=150, height=150)
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
        width = 0.8
        fig = plt.Figure(figsize=(2, 2), dpi=75)
        ax = fig.subplots()
        ax.bar(labels, follower_counts, width, color='b')
        ax.bar(labels, amulet_counts, width, bottom=follower_counts, color='g')
        ax.bar(labels, spell_counts, width, bottom=fa_counts, color='r')
        ax.yaxis.set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)
        background_color = hf.rgb_to_hex(self.frame.winfo_rgb(self.frame['bg']))
        ax.set_facecolor(background_color)
        ax.set_title('Cost Breakdown')

        fig.patch.set_facecolor(background_color)

        cost_chart = FigureCanvasTkAgg(fig, self.frame)
        cost_chart.get_tk_widget().pack(fill=BOTH)
        return cost_chart

    def resize(self, event):
        self.frame.configure(width=event.width, height=event.width)

