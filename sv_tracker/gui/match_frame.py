from tkinter import *
from PIL import ImageTk
from sv_tracker.class_icons import ClassIcons

FONT = 'times 14'


class MatchFrame(Frame):
    def __init__(self, master, match):
        self.match = match
        super().__init__(master)

        self.clan_icon = None
        self.tk_image = None
        self.clan_label = self.generate_clan_label()

        self.first_label = Label(self, width=9, font=FONT)
        self.won_label = Label(self, width=5, font=FONT)

        minutes = int(self.match['duration'] / 60)
        seconds = int(self.match['duration'] % 60)
        duration_text = str(minutes) + 'm ' + str(seconds) + 's'
        self.duration_label = Label(self, text=duration_text, width=10, font=FONT)

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
            1: 'forest',
            2: 'sword',
            3: 'rune',
            4: 'dragon',
            5: 'shadow',
            6: 'blood',
            7: 'haven',
            8: 'portal'
        }
        self.clan_icon = ClassIcons().get_icon(classes.get(self.match['class']))
        img_copy = self.clan_icon.resize((25, 25))
        self.tk_image = ImageTk.PhotoImage(img_copy)

        label = Label(self, image=self.tk_image)
        return label

    def adjust_widgets(self):
        self.clan_label.grid(row=0, column=0)
        self.first_label.grid(row=0, column=1)
        self.won_label.grid(row=0, column=2)
        self.duration_label.grid(row=0, column=3)