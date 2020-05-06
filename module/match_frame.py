from tkinter import *


class MatchFrame:
    def __init__(self, master, match):
        self.match = match
        self.frame = Frame(master, width=300, height=100, bd=1, relief=GROOVE)
        self.clan_label = self.generate_clan_label()
        self.first_label = Label(self.frame)
        self.won_label = Label(self.frame)

        minutes = int(self.match['duration'] / 60)
        seconds = int(self.match['duration'] % 60)
        duration_text = str(minutes) + 'm ' + str(seconds) + 's'
        self.duration_label = Label(self.frame, text=duration_text)

        if self.match['first']:
            self.first_label.configure(text="FIRST")
        else:
            self.first_label.configure(text="SECOND")

        if self.match['won']:
            self.won_label.configure(text="WIN")
        else:
            self.won_label.configure(text="LOSS")

        self.adjust_widgets()

    def generate_clan_label(self):
        classes = {
            1: 'Forest',
            2: 'Sword',
            3: 'Rune',
            4: 'Dragon',
            5: 'Shadow',
            6: 'Blood',
            7: 'Haven',
            8: 'Portal'
        }
        label = Label(self.frame, text=classes.get(self.match['class']))
        return label

    def adjust_widgets(self):
        self.clan_label.grid(row=0, column=0)
        self.first_label.grid(row=0, column=1)
        self.won_label.grid(row=0, column=2)
        self.duration_label.grid(row=0, column=3)
