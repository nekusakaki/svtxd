from tkinter import *
from deck import Deck
from decklist_frame import DecklistFrame


root = Tk()
root.title("SV Deck Tracker XD")

deck = Deck.generate_from_file('../decks/Machina_Forest.dck')
decklist_frame = DecklistFrame(root, deck)
dl_frame = decklist_frame.frame()

dl_frame.grid(row=0, column=0, padx=10, pady=10, sticky=E+W+N)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.resizable(width=True, height=False)

root.geometry("")

root.mainloop()
