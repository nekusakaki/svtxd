from tkinter import *
from sv_tracker.gui.main_frame import MainFrame
import matplotlib


def main():
    matplotlib.use("Agg")

    root = Tk()
    root.title("SV Deck Tracker XD")

    main_frame = MainFrame(root)
    main_frame.frame.pack()

    root.resizable(width=False, height=False)

    root.mainloop()


if __name__ == "__main__":
    main()
