from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
from sv_tracker.gui.splash_screen import SplashScreen
from sv_tracker.deck import Deck
from sv_tracker.gui.deck_list_frame import DeckListFrame
from sv_tracker.gui.deck_preview_frame import DeckPreviewFrame
from sv_tracker.gui.add_deck_frame import AddDeckFrame
from sv_tracker.gui.stats_frame import StatsFrame
from sv_tracker.gui.deck_tracker_frame import DeckTrackerFrame

DECK_FOLDER = 'decks/'


class MainFrame:
    def __init__(self, master):
        master.withdraw()
        self.splash_screen = SplashScreen(master)
        self.decks = self.load_decks(DECK_FOLDER)
        self.decks_sorted = self.sort_decks()
        self.displayed_decks = self.decks
        self.deck_previews = {}
        self.current_clan = 'All'
        self.current_deck = None

        self.frame = Frame(master, width=715, height=577)
        self.add_deck_button = ttk.Button(self.frame, text="ADD DECK", command=self.add_deck_popup)
        self.sort_buttons_frame = Frame(self.frame)
        self.decks_canvas = Canvas(self.frame, width=300, scrollregion=(0, 0, 300, 500), highlightthickness=0)
        self.decks_frame = Frame(self.decks_canvas, height=500, bd=0, borderwidth=0)
        self.vbar = ttk.Scrollbar(self.frame, orient=VERTICAL)

        self.add_popup = None

        self.start_button = ttk.Button(self.frame, text="START DECK TRACKER", command=self.start)
        self.deck_tracker = None
        self.deck_tracker_frame = None

        self.deck_notebook = ttk.Notebook(self.frame)
        self.tab_frame_0 = Frame(self.deck_notebook, width=320, height=500)
        self.tab_frame_1 = Frame(self.deck_notebook, width=320, height=500)
        self.deck_list_frame = Frame(self.tab_frame_0, width=320, height=500)
        self.stats_frame = Frame(self.tab_frame_0, width=320, height=500)

        self.fill_sort_buttons_frame()
        self.generate_deck_previews()
        self.fill_decks_frame()
        self.adjust_widgets()

        self.splash_screen.destroy()
        master.deiconify()

    def start(self):
        if self.current_deck is None:
            messagebox.showinfo('Error', 'Please choose a deck.')
            return

        if self.deck_tracker and self.deck_tracker.winfo_exists() \
                and self.deck_tracker_frame.deck is self.current_deck:
            self.deck_tracker.focus_set()
            return

        if self.deck_tracker and self.deck_tracker.winfo_exists() \
                and self.deck_tracker_frame.deck is not self.current_deck:
            switch_decks = messagebox.askyesno('Warning', 'Switch decks?')
            if switch_decks:
                self.deck_tracker.destroy()
                self.deck_tracker = None
            else:
                return

        self.deck_tracker = Toplevel()
        self.deck_tracker.title(self.current_deck.name)
        self.deck_tracker.resizable(True, False)
        self.deck_tracker.attributes('-topmost', 'true')
        self.deck_tracker.focus_set()

        self.deck_tracker_frame = DeckTrackerFrame(self.deck_tracker, self.current_deck, self.refresh, self.save_deck)
        self.deck_tracker_frame.frame.pack(fill=BOTH, expand=TRUE)
        self.deck_tracker_frame.frame.bind('<Configure>', self.deck_tracker_frame.resize)

    def add_deck_popup(self):
        if self.add_popup:
            self.add_popup.destroy()

        self.add_popup = Toplevel()
        add_deck_frame = AddDeckFrame(self.add_popup, self.add_deck)
        add_deck_frame.pack()
        self.add_popup.focus_set()

    def add_deck(self, deck):
        self.save_deck(deck)
        self.decks.append(deck)
        self.deck_previews[deck] = DeckPreviewFrame(self.decks_frame, deck, self.view_deck)
        self.decks_sorted = self.sort_decks()

        self.add_popup.destroy()
        self.add_popup = None

        self.show_clan_decks(self.current_clan)

    def save_deck(self, deck):
        if not os.path.exists(DECK_FOLDER):
            os.makedirs(DECK_FOLDER)

        deck.save_to_file(DECK_FOLDER)

    def load_decks(self, folder_path):
        decks = []
        deck_paths = []

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for root, directories, files in os.walk(folder_path):
            for file in files:
                if '.deck' in file:
                    deck_paths.append(folder_path + file)

        for path in deck_paths:
            decks.append(Deck.generate_from_file(path))

        return decks

    def sort_decks(self):
        decks_sorted = {'Forest': [], 'Sword': [], 'Rune': [], 'Dragon': [],
                        'Shadow': [], 'Blood': [], 'Haven': [], 'Portal': []}

        for deck in self.decks:
            decks_sorted[deck.clan()].append(deck)

        return decks_sorted

    def fill_sort_buttons_frame(self):
        button = ttk.Button(self.sort_buttons_frame, text='All', command=lambda: self.show_clan_decks('All'))
        button.grid(row=0, column=0, rowspan=2, sticky=N+E+W+S)
        button1 = ttk.Button(self.sort_buttons_frame, text='Forest', command=lambda: self.show_clan_decks('Forest'))
        button1.grid(row=0, column=1)
        button2 = ttk.Button(self.sort_buttons_frame, text='Sword', command=lambda: self.show_clan_decks('Sword'))
        button2.grid(row=0, column=2)
        button3 = ttk.Button(self.sort_buttons_frame, text='Rune', command=lambda: self.show_clan_decks('Rune'))
        button3.grid(row=0, column=3)
        button4 = ttk.Button(self.sort_buttons_frame, text='Dragon', command=lambda: self.show_clan_decks('Dragon'))
        button4.grid(row=0, column=4)
        button5 = ttk.Button(self.sort_buttons_frame, text='Shadow', command=lambda: self.show_clan_decks('Shadow'))
        button5.grid(row=1, column=1)
        button6 = ttk.Button(self.sort_buttons_frame, text='Blood', command=lambda: self.show_clan_decks('Blood'))
        button6.grid(row=1, column=2)
        button7 = ttk.Button(self.sort_buttons_frame, text='Haven', command=lambda: self.show_clan_decks('Haven'))
        button7.grid(row=1, column=3)
        button8 = ttk.Button(self.sort_buttons_frame, text='Portal', command=lambda: self.show_clan_decks('Portal'))
        button8.grid(row=1, column=4)

    def show_clan_decks(self, clan):
        if clan == 'All':
            self.displayed_decks = self.decks
        else:
            self.displayed_decks = self.decks_sorted[clan]

        self.current_clan = clan

        for child in self.decks_frame.winfo_children():
            child.pack_forget()
        self.fill_decks_frame()

        bbox = self.decks_canvas.bbox('all')

        if bbox is None:
            self.decks_canvas.configure(scrollregion=(0, 0, 0, 0))
        else:
            self.decks_canvas.configure(scrollregion=bbox)

    def decks_frame_resize(self, event):
        self.decks_canvas.configure(scrollregion=self.decks_canvas.bbox('all'))

    def refresh(self):
        self.generate_deck_previews()

        for child in self.decks_frame.winfo_children():
            child.pack_forget()
        self.fill_decks_frame()

        deck = self.current_deck
        self.current_deck = None
        if deck is not None:
            self.view_deck(deck)

    def generate_deck_previews(self):
        self.deck_previews.clear()

        for deck in self.decks:
            self.deck_previews[deck] = DeckPreviewFrame(self.decks_frame, deck, self.view_deck)

    def fill_decks_frame(self):
        for deck in self.displayed_decks:
            deck_preview = self.deck_previews[deck]
            deck_preview.frame.pack(side=TOP, fill=X, expand=TRUE, padx=5, pady=5)

    def view_deck(self, deck):
        if deck == self.current_deck:
            return

        self.deck_previews[deck].select()
        if self.current_deck:
            self.deck_previews[self.current_deck].deselect()
            for child in self.tab_frame_0.winfo_children():
                child.destroy()
            for child in self.tab_frame_1.winfo_children():
                child.destroy()

        self.deck_list_frame.destroy()
        self.stats_frame.destroy()

        self.current_deck = deck

        self.preview_deck()
        self.preview_stats()

    def preview_deck(self):
        self.deck_list_frame = DeckListFrame(self.tab_frame_0, self.current_deck)
        self.deck_list_frame.frame.grid(row=0, column=0, sticky=N+E+W+S)

    def preview_stats(self):
        self.stats_frame = StatsFrame(self.tab_frame_1, self.current_deck, self.refresh)
        self.stats_frame.frame.grid(row=0, column=0, sticky=N+E+W+S)

    def adjust_widgets(self):
        self.add_deck_button.grid(row=0, column=0, columnspan=2, sticky=W+E)

        self.sort_buttons_frame.grid(row=1, column=0, columnspan=2, sticky=N+E+W+S)

        self.decks_canvas.grid(row=2, column=0, sticky=N+E+W+S)
        self.decks_canvas.configure(yscrollcommand=self.vbar.set)
        self.decks_canvas.create_window((0, 0), window=self.decks_frame, width=363, anchor=N+W)
        self.decks_canvas.bind('<Enter>', self.bind_mousewheel)
        self.decks_canvas.bind('<Leave>', self.unbind_mousewheel)

        self.decks_frame.bind('<Configure>', self.decks_frame_resize)

        self.vbar.grid(row=2, column=1, sticky=N+S+E)
        self.vbar.configure(command=self.decks_canvas.yview)

        self.start_button.grid(row=0, column=2, sticky=W+E)

        self.deck_notebook.grid(row=1, column=2, rowspan=2, sticky=N+E+W+S)
        self.tab_frame_0.pack(fill=BOTH, expand=True)
        self.tab_frame_1.pack(fill=BOTH, expand=True)

        self.deck_list_frame.grid(row=0, column=0, sticky=N+E+W+S)

        self.stats_frame.grid(row=0, column=0, sticky=N+E+W+S)

        self.deck_notebook.add(self.tab_frame_0, text='Decklist')
        self.deck_notebook.add(self.tab_frame_1, text='Match Statistics')

        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=0)
        self.frame.rowconfigure(2, weight=1)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=0)
        self.frame.grid_propagate(False)

    def bind_mousewheel(self, event):
        self.decks_canvas.bind_all('<MouseWheel>', self.on_mousewheel)

    def unbind_mousewheel(self, event):
        self.decks_canvas.unbind_all('<MouseWheel>')

    def on_mousewheel(self, event):
        self.decks_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
