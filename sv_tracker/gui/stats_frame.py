from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from sv_tracker.class_icons import ClassIcons
from sv_tracker.gui.edit_matches_frame import EditMatchesFrame
from sv_tracker.gui.graphs.match_breakdown_frame import MatchBreakdownFrame
from sv_tracker.gui.graphs.wins_breakdown_frame import WinsBreakdownFrame
from sv_tracker.gui.match_history_frame import MatchHistoryFrame
from sv_tracker.gui.graphs.losses_breakdown_frame import LossesBreakdownFrame
from sv_tracker.gui.graphs.first_breakdown_frame import FirstBreakdownFrame
from sv_tracker.gui.graphs.second_breakdown_frame import SecondBreakdownFrame


class StatsFrame(Frame):
    def __init__(self, master, deck, refresh):
        self.deck = deck
        self.refresh = refresh

        super().__init__(master, width=320, height=500, padx=5, pady=5)

        self.class_icon = ClassIcons().get_icon(self.deck.clan())
        self.resized_image = self.class_icon.resize((50, 50))
        self.tk_image = ImageTk.PhotoImage(self.resized_image)
        self.deck_name_label = Label(self, image=self.tk_image, text=self.deck.name, bg="black",
                                     fg="white", compound=RIGHT, anchor=E, font="Sans 12 bold")

        self.edit_window = None
        self.edit_matches_frame = None
        self.edit_matches = ttk.Button(self, text="EDIT MATCHES", command=self.edit)

        self.figures_notebook = ttk.Notebook(self)
        self.match_breakdown_frame = MatchBreakdownFrame(self.figures_notebook, self.deck)
        self.wins_breakdown_frame = WinsBreakdownFrame(self.figures_notebook, self.deck)
        self.losses_breakdown_frame = LossesBreakdownFrame(self.figures_notebook, self.deck)
        self.first_breakdown_frame = FirstBreakdownFrame(self.figures_notebook, self.deck)
        self.second_breakdown_frame = SecondBreakdownFrame(self.figures_notebook, self.deck)

        self.match_history_frame = MatchHistoryFrame(self, self.deck)

        self.adjust_widgets()

    def edit(self):
        self.edit_window = Toplevel()
        self.edit_matches_frame = EditMatchesFrame(self.edit_window, self.deck, self.refresh)
        self.edit_matches_frame.pack()

    def adjust_widgets(self):
        self.deck_name_label.grid(row=0, column=0, sticky=E+W)

        self.match_breakdown_frame.pack(fill=BOTH, expand=True)
        self.wins_breakdown_frame.frame.pack(fill=BOTH, expand=True)
        self.losses_breakdown_frame.pack(fill=BOTH, expand=True)
        self.first_breakdown_frame.pack(fill=BOTH, expand=True)
        self.second_breakdown_frame.frame.pack(fill=BOTH, expand=True)

        self.match_history_frame.grid(row=2, column=0, sticky=N+E+W+S, pady=5)

        self.figures_notebook.grid(row=1, column=0, sticky=E+W, pady=5)
        self.figures_notebook.add(self.match_breakdown_frame, text='Opponents')
        self.figures_notebook.add(self.wins_breakdown_frame.frame, text='Wins')
        self.figures_notebook.add(self.losses_breakdown_frame, text='Losses')
        self.figures_notebook.add(self.first_breakdown_frame, text='First')
        self.figures_notebook.add(self.second_breakdown_frame.frame, text='Second')

        self.edit_matches.grid(row=3, column=0, sticky=N+E+W+S, padx=5, pady=5)

    def destroy(self):
        if self.edit_matches:
            self.edit_matches.destroy()
            self.edit_matches = None

        self.match_breakdown_frame.destroy()
        self.wins_breakdown_frame.destroy()
        self.losses_breakdown_frame.destroy()
        self.first_breakdown_frame.destroy()
        self.second_breakdown_frame.destroy()

        super().destroy()
