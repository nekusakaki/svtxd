from tkinter import *
from tkinter import messagebox
from tkinter import ttk


class EditMatchesFrame(Frame):
    def __init__(self, master, deck, refresh):
        self.deck = deck
        self.refresh = refresh

        super().__init__(master, padx=5, pady=5)
        self.list_box = Listbox(self, width=30)
        self.delete_button = ttk.Button(self, text="DELETE MATCH", command=self.delete_match)

        self.fill_listbox()

        self.adjust_widgets()

    def delete_match(self):
        match_index = self.list_box.curselection()[0]
        self.delete_button.config(state=DISABLED)

        confirm = messagebox.askyesno('Delete Match', 'Are you sure you want to delete this match?')

        if not confirm:
            self.delete_button.config(state=NORMAL)
            self.focus_set()
            return

        self.deck.delete_match(match_index)
        self.refresh_listbox()
        self.refresh()
        self.delete_button.config(state=NORMAL)
        self.deck.save_to_file('decks/')
        self.focus_set()

    def fill_listbox(self):
        for index, match in enumerate(self.deck.get_matches()):
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

            vs = classes.get(match['class']) + ' '
            first = ('FIRST' if match['first'] else 'SECOND') + ' '
            won = ('WIN' if match['won'] else 'LOSE') + ' '
            minutes = int(match['duration'] / 60)
            seconds = int(match['duration'] % 60)
            duration_text = str(minutes) + 'm ' + str(seconds) + 's'
            self.list_box.insert(index, str(index + 1) + ': ' + vs + first + won + duration_text)

    def refresh_listbox(self):
        self.list_box.delete(0, END)
        self.fill_listbox()

    def adjust_widgets(self):
        self.list_box.grid(row=0, column=0)
        self.delete_button.grid(row=1, column=0)
