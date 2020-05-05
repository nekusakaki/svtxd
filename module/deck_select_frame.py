from tkinter import *
from tkinter import messagebox
from deck import Deck
from decklist_frame import DecklistFrame
from deck_preview_frame import DeckPreviewFrame
import os


class DeckSelectFrame:
    def __init__(self, master):
        self.decks = self.load_decks('../decks/')
        self.decks_sorted = self.sort_decks()
        self.displayed_decks = self.decks
        self.deck_previews = {}
        self.current_clan = 'All'
        self.current_deck = None

        self.frame = Frame(master, width=300, height=300)
        self.add_deck_button = Button(self.frame, text="ADD DECK", command=self.add_deck_popup)
        self.sort_buttons_frame = Frame(self.frame)
        self.decks_canvas = Canvas(self.frame, width=300, scrollregion=(0, 0, 300, 500))
        self.decks_frame = Frame(self.decks_canvas, height=500, bd=0, borderwidth=0)
        self.vbar = Scrollbar(self.frame, orient=VERTICAL)

        self.add_popup = None

        self.decklist_frame = None

        self.fill_sort_buttons_frame()
        self.generate_deck_previews()
        self.fill_decks_frame()
        self.adjust_widgets()

    def add_deck_popup(self):
        if self.add_popup:
            self.add_popup.destroy()

        self.add_popup = Toplevel()
        add_deck_frame = AddDeckFrame(self.add_popup, self.add_deck)
        add_deck_frame.frame.pack()

    def add_deck(self, deck):
        deck.save_to_file('../decks/')
        self.decks.append(deck)
        self.deck_previews[deck] = DeckPreviewFrame(self.decks_frame, deck, self.view_deck)
        self.decks_sorted = self.sort_decks()

        self.add_popup.destroy()
        self.add_popup = None

        self.show_clan_decks(self.current_clan)

    def load_decks(self, folder_path):
        decks = []
        deck_paths = []

        for root, directories, files in os.walk(folder_path):
            for file in files:
                if '.dck' in file:
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
        # clans = ['All', 'Forest', 'Sword', 'Rune', 'Dragon', 'Shadow', 'Blood', 'Haven', 'Portal']
        #
        # for clan in clans:
        #     button = Button(self.sort_buttons_frame, text=clan, command=lambda: self.show_clan_decks(clan))
        #     button.pack(side=LEFT)
        button = Button(self.sort_buttons_frame, text='All', command=lambda: self.show_clan_decks('All'))
        button.pack(side=LEFT)
        button1 = Button(self.sort_buttons_frame, text='Forest', command=lambda: self.show_clan_decks('Forest'))
        button1.pack(side=LEFT)
        button2 = Button(self.sort_buttons_frame, text='Sword', command=lambda: self.show_clan_decks('Sword'))
        button2.pack(side=LEFT)
        button3 = Button(self.sort_buttons_frame, text='Rune', command=lambda: self.show_clan_decks('Rune'))
        button3.pack(side=LEFT)
        button4 = Button(self.sort_buttons_frame, text='Dragon', command=lambda: self.show_clan_decks('Dragon'))
        button4.pack(side=LEFT)
        button5 = Button(self.sort_buttons_frame, text='Shadow', command=lambda: self.show_clan_decks('Shadow'))
        button5.pack(side=LEFT)
        button6 = Button(self.sort_buttons_frame, text='Blood', command=lambda: self.show_clan_decks('Blood'))
        button6.pack(side=LEFT)
        button7 = Button(self.sort_buttons_frame, text='Haven', command=lambda: self.show_clan_decks('Haven'))
        button7.pack(side=LEFT)
        button8 = Button(self.sort_buttons_frame, text='Portal', command=lambda: self.show_clan_decks('Portal'))
        button8.pack(side=LEFT)

    def show_clan_decks(self, clan):
        if clan == 'All':
            self.displayed_decks = self.decks
        else:
            self.displayed_decks = self.decks_sorted[clan]

        self.current_clan = clan

        for child in self.decks_frame.winfo_children():
            child.grid_forget()
        self.fill_decks_frame()

    def decks_frame_resize(self, event):
        self.decks_canvas.configure(scrollregion=self.decks_canvas.bbox('all'))

    def generate_deck_previews(self):
        self.deck_previews.clear()

        for deck in self.decks:
            self.deck_previews[deck] = DeckPreviewFrame(self.decks_frame, deck, self.view_deck)

    def fill_decks_frame(self):
        for index, deck in enumerate(self.displayed_decks):
            deck_preview = self.deck_previews[deck]
            deck_preview.frame.grid(row=index, column=0, sticky=W+E)

    def view_deck(self, deck):
        self.current_deck = deck
        self.preview_deck()

    def preview_deck(self):
        if self.decklist_frame:
            self.decklist_frame.delete()

        self.decklist_frame = DecklistFrame(self.frame, self.current_deck)
        self.decklist_frame.frame.grid(row=2, column=2, sticky=N+E+W+S)

    def adjust_widgets(self):
        self.add_deck_button.grid(row=0, column=0, columnspan=2)

        self.sort_buttons_frame.grid(row=1, column=0, columnspan=2, sticky=N+E+W+S)

        self.decks_canvas.grid(row=2, column=0, sticky=N+E+W+S)
        self.decks_canvas.configure(yscrollcommand=self.vbar.set)
        self.decks_canvas.create_window((0, 0), window=self.decks_frame, anchor=N+W)

        self.decks_frame.bind('<Configure>', self.decks_frame_resize)

        self.vbar.grid(row=2, column=1, sticky=N+S)
        self.vbar.configure(command=self.decks_canvas.yview)


class AddDeckFrame:
    def __init__(self, master, function):
        self.add_deck_function = function

        self.frame = Frame(master)
        self.deck_name_label = Label(self.frame, text="Deck Name: ")
        self.deck_name_entry = Entry(self.frame, width=30)
        self.deck_code_label = Label(self.frame, text="Deck Code: ")
        self.deck_code_entry = Entry(self.frame, width=4)
        self.enter_button = Button(self.frame, text='Enter', command=self.add_deck)

        self.adjust_widgets()

    def add_deck(self):
        deck_name = self.deck_name_entry.get()
        deck_code = self.deck_code_entry.get()

        if not deck_name:
            messagebox.showinfo("Error", "Invalid deck name.")
            return

        if not len(deck_code) == 4:
            messagebox.showinfo("Error", "Invalid deck code.")
            return

        deck = Deck.generate_from_deck_code(deck_name, deck_code)
        if not deck:
            messagebox.showinfo("Error", "Invalid or expired deck code.")
            return

        self.add_deck_function(deck)

    def adjust_widgets(self):
        self.deck_name_label.grid(row=0, column=0)

        self.deck_name_entry.grid(row=0, column=1)

        self.deck_code_label.grid(row=1, column=0)

        self.deck_code_entry.grid(row=1, column=1)

        self.enter_button.grid(row=2, column=0, columnspan=2)
