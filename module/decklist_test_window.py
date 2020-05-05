from tkinter import *
from deck_select_frame import DeckSelectFrame


root = Tk()
root.title("SV Deck Tracker XD")

deck_select_frame = DeckSelectFrame(root)

deck_select_frame.frame.pack()

# root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

root.resizable(width=True, height=False)

# root.geometry("")

root.mainloop()
