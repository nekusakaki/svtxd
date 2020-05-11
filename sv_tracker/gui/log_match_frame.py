from tkinter import *
from tkinter import ttk


class LogMatchFrame:
    def __init__(self, master, stopwatch, log_function):
        self.frame = Frame(master)
        self.stopwatch = stopwatch
        self.function = log_function

        self.won_label = Label(self.frame, text='Won?')
        self.won = BooleanVar()
        self.won.set(True)
        self.win = Radiobutton(self.frame, text='Win', variable=self.won, value=True)
        self.lose = Radiobutton(self.frame, text='Lose', variable=self.won, value=False)

        self.first_label = Label(self.frame, text='First?')
        self.is_first = BooleanVar()
        self.is_first.set(True)
        self.first = Radiobutton(self.frame, text='First', variable=self.is_first, value=True)
        self.second = Radiobutton(self.frame, text='Second', variable=self.is_first, value=False)

        self.against_label = Label(self.frame, text='Against?')
        self.clan = IntVar()
        self.clan.set(1)
        self.clan_frame = Frame(self.frame)
        self.forest = Radiobutton(self.clan_frame, text='Forest', variable=self.clan, value=1)
        self.sword = Radiobutton(self.clan_frame, text='Sword', variable=self.clan, value=2)
        self.rune = Radiobutton(self.clan_frame, text='Rune', variable=self.clan, value=3)
        self.dragon = Radiobutton(self.clan_frame, text='Dragon', variable=self.clan, value=4)
        self.shadow = Radiobutton(self.clan_frame, text='Shadow', variable=self.clan, value=5)
        self.blood = Radiobutton(self.clan_frame, text='Blood', variable=self.clan, value=6)
        self.haven = Radiobutton(self.clan_frame, text='Haven', variable=self.clan, value=7)
        self.portal = Radiobutton(self.clan_frame, text='Portal', variable=self.clan, value=8)

        self.duration = self.stopwatch.get_duration()
        self.duration_label = Label(self.frame,
                                    text='Duration: {:02d}:{:02d}'.format(int(self.duration / 60),
                                                                          int(self.duration % 60)))

        self.log_button = ttk.Button(self.frame, text='Log', command=self.log)

        self.adjust_widgets()

    def log(self):
        self.function(self.won.get(), self.clan.get(), self.is_first.get(), self.duration)

    def adjust_widgets(self):
        self.won_label.grid(row=0, column=0, columnspan=2, pady=5)
        self.win.grid(row=1, column=0)
        self.lose.grid(row=1, column=1)

        self.first_label.grid(row=2, column=0, columnspan=2, pady=5)
        self.first.grid(row=3, column=0)
        self.second.grid(row=3, column=1)

        self.against_label.grid(row=4, column=0, columnspan=2, pady=5)
        self.clan_frame.grid(row=5, column=0, columnspan=2)

        self.forest.grid(row=0, column=0)
        self.sword.grid(row=0, column=1)
        self.rune.grid(row=0, column=2)
        self.dragon.grid(row=0, column=3)
        self.shadow.grid(row=1, column=0)
        self.blood.grid(row=1, column=1)
        self.haven.grid(row=1, column=2)
        self.portal.grid(row=1, column=3)

        self.duration_label.grid(row=6, column=0, columnspan=2, sticky=N+E+W+S, pady=5)

        self.log_button.grid(row=7, column=0, columnspan=2, sticky=N+E+W+S, padx=5, pady=5)