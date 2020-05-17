from tkinter import *


class SplashScreen(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.wm_overrideredirect(True)

        self.label = Label(self, text='LOADING', font='fixedsys 20 bold')
        self.label.pack()

        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()

        top_left_x = int(master.winfo_screenwidth()/2 - width/2)
        top_left_y = int(master.winfo_screenheight()/2 - height/2)

        self.geometry("+{}+{}".format(top_left_x, top_left_y))

        self.update()

    def destroy(self):
        super().destroy()