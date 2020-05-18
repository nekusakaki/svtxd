from tkinter import *
from sv_tracker.gui.main_frame import MainFrame
import matplotlib

TITLE = 'SV Deck Tracker'


def main():
    matplotlib.use("Agg")

    root = Tk()
    root.title(TITLE)

    main_frame = MainFrame(root)
    main_frame.pack()

    root.resizable(width=False, height=False)

    root.mainloop()


if __name__ == "__main__":
    main()
