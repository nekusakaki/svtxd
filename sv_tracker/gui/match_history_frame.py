from tkinter import *
from sv_tracker.gui.match_frame import MatchFrame


class MatchHistoryFrame:
    def __init__(self, master, deck):
        self.deck = deck
        self.frame = Frame(master, width=300, height=150)
        self.canvas = Canvas(self.frame, width=300, height=150, scrollregion=(0, 0, 320, 500))
        self.vbar = Scrollbar(self.frame, orient=VERTICAL)
        self.matches_frame = Frame(self.canvas, width=300)
        self.matches = []

        self.fill_matches_frame()
        self.adjust_widgets()

    def fill_matches_frame(self):
        match_history = self.deck.get_matches()

        for index, match in enumerate(match_history):
            match_preview = MatchFrame(self.matches_frame, match)
            match_preview.frame.grid(row=index, column=0, sticky=W+E, pady=5)
            self.matches.append(match_preview)

    def adjust_widgets(self):
        self.vbar.grid(row=0, column=1, sticky=N+S)
        self.vbar.configure(command=self.canvas.yview)

        self.canvas.grid(row=0, column=0, sticky=N+E+W+S)
        self.canvas.create_window((0, 0), window=self.matches_frame, anchor=N)
        self.canvas.configure(yscrollcommand=self.vbar.set)
        self.canvas.bind('<Enter>', self.bind_mousewheel)
        self.canvas.bind('<Leave>', self.unbind_mousewheel)

        self.frame.bind('<Configure>', self.resize)

    def resize(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def bind_mousewheel(self, event):
        self.canvas.bind_all('<MouseWheel>', self.on_mousewheel)

    def unbind_mousewheel(self, event):
        self.canvas.unbind_all('<MouseWheel>')

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")