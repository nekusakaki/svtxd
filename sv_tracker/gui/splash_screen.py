from tkinter import *


class SplashScreen:
    def __init__(self, master):
        self.toplevel = Toplevel(master)
        self.toplevel.wm_overrideredirect(True)

        self.label = Label(self.toplevel, text='LOADING', font='fixedsys 20 bold')
        self.label.pack()

        width = self.toplevel.winfo_reqwidth()
        height = self.toplevel.winfo_reqheight()

        top_left_x = int(master.winfo_screenwidth()/2 - width/2)
        top_left_y = int(master.winfo_screenheight()/2 - height/2)

        self.toplevel.geometry("+{}+{}".format(top_left_x, top_left_y))

        self.toplevel.update()

    def destroy(self):
        self.toplevel.destroy()