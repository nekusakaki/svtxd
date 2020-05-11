from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from sv_tracker.class_icons import ClassIcons


class DeckPreviewFrame:
    def __init__(self, master, deck, function):
        self.deck = deck

        self.function = function

        self.class_icon = ClassIcons().get_icon(self.deck.clan())
        self.resized_image = self.class_icon.resize((50, 50))
        self.tk_image = ImageTk.PhotoImage(self.resized_image)

        self.frame = Frame(master)
        self.icon_label = Label(self.frame, image=self.tk_image)
        self.deck_name_label = Label(self.frame, text=self.deck.name, anchor=W, font="Arial 14")
        self.stats_label = self.generate_stats_label(self.frame)

        self.adjust_widgets()

    def generate_stats_label(self, master):
        text = ""
        if self.deck.wins() + self.deck.losses() == 0:
            text = "No Stats"
        else:
            win_rate = '{:.2f}'.format(self.deck.win_rate())
            text = win_rate + ' | ' + str(self.deck.wins()) + '-' + str(self.deck.losses())
        label = Label(master, text=text, anchor=W)
        return label

    def view_deck(self, event):
        self.function(self.deck)

    def adjust_widgets(self):
        self.icon_label.grid(row=0, column=0, rowspan=2, sticky=N+E+W+S)
        self.deck_name_label.grid(row=0, column=1, sticky=E+W, padx=10)
        self.stats_label.grid(row=1, column=1, sticky=E+W, padx=10)

        self.frame.bind('<Enter>', self.bind_left_click)
        self.frame.bind('<Leave>', self.unbind_left_click)

    def bind_left_click(self, event):
        self.frame.bind_all('<Button-1>', self.view_deck)

    def unbind_left_click(self, event):
        self.frame.unbind_all('<Button-1>')

    def select(self):
        class_color = {
            'Forest': '#339900',
            'Sword': '#D7CD4C',
            'Rune': '#333399',
            'Dragon': '#CC6633',
            'Shadow': '#9D87DE',
            'Blood': '#990033',
            'Haven': '#B0A979',
            'Portal': '#41ACE1',
        }

        bg_color = class_color.get(self.deck.clan())

        self.frame.config(bg=bg_color)
        self.icon_label.config(bg=bg_color)
        self.deck_name_label.config(bg=bg_color, fg='white')
        self.stats_label.config(bg=bg_color, fg='white')

    def deselect(self):
        self.frame.config(bg='SystemButtonFace')
        self.icon_label.config(bg=self.frame['bg'])
        self.deck_name_label.config(bg=self.frame['bg'], fg='black')
        self.stats_label.config(bg=self.frame['bg'], fg='black')
