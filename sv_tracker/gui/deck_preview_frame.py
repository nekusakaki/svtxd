from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
from sv_tracker.class_icons import ClassIcons


class DeckPreviewFrame(Frame):
    def __init__(self, master, deck, view_function, delete_function):
        self.deck = deck

        self.view_function = view_function
        self.delete_function = delete_function

        self.class_icon = ClassIcons().get_icon(self.deck.clan())
        self.resized_image = self.class_icon.resize((50, 50))
        self.tk_image = ImageTk.PhotoImage(self.resized_image)

        super().__init__(master)
        self.icon_label = Label(self, image=self.tk_image)
        self.deck_name_label = Label(self, text=self.deck.name, anchor=W, font="Arial 14")
        self.stats_label = self.generate_stats_label(self)

        self.popup_menu = Menu(self, tearoff=0)
        self.popup_menu.add_command(label='Delete Deck', command=self.delete_deck)

        self.adjust_widgets()

    def generate_stats_label(self, master):
        text = ""
        if self.deck.wins() + self.deck.losses() == 0:
            text = "No Stats"
        else:
            win_rate = '{:.2f}'.format(self.deck.win_rate())
            text = win_rate + '% | ' + str(self.deck.wins()) + '-' + str(self.deck.losses())
        label = Label(master, text=text, anchor=W)
        return label

    def view_deck(self, event):
        self.view_function(self.deck)

    def delete_deck(self):
        confirm = messagebox.askyesno('Delete Deck',
                                      'Are you sure you want to delete ' + self.deck.name + '?')

        if confirm:
            self.delete_function(self.deck)

    def adjust_widgets(self):
        self.icon_label.grid(row=0, column=0, rowspan=2, sticky=N+E+W+S)
        self.deck_name_label.grid(row=0, column=1, sticky=E+W, padx=10)
        self.stats_label.grid(row=1, column=1, sticky=E+W, padx=10)

        self.bind('<Enter>', self.bind_click)
        self.bind('<Leave>', self.unbind_click)

    def bind_click(self, event):
        self.bind_all('<Button-1>', self.view_deck)
        self.bind_all('<Button-3>', self.popup)

    def popup(self, event):
        self.popup_menu.post(event.x_root, event.y_root)

    def unbind_click(self, event):
        self.unbind_all('<Button-1>')
        self.unbind_all('<Button-3>')

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

        self.config(bg=bg_color)
        self.icon_label.config(bg=bg_color)
        self.deck_name_label.config(bg=bg_color, fg='white')
        self.stats_label.config(bg=bg_color, fg='white')

    def deselect(self):
        self.config(bg=self.master['bg'])
        self.icon_label.config(bg=self['bg'])
        self.deck_name_label.config(bg=self['bg'], fg='black')
        self.stats_label.config(bg=self['bg'], fg='black')
