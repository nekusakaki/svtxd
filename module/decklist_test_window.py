from tkinter import *
from gui.main_frame import MainFrame
import matplotlib


matplotlib.use("Agg")

root = Tk()
root.title("SV Deck Tracker XD")

main_frame = MainFrame(root)

main_frame.frame.pack()

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

root.resizable(width=False, height=False)

# root.geometry("")

root.mainloop()
