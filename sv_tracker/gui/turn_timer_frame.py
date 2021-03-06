from tkinter import *


class TurnTimerFrame(Frame):
    TURN_SECONDS = 90

    def __init__(self, master):
        self.seconds = self.TURN_SECONDS

        self.job = None

        super().__init__(master)
        self.time_label = Label(self, text=self.seconds, font='times 20')

        self.start_button = Button(self, text='START', command=self.start)
        self.stop_button = Button(self, text='STOP', command=self.stop)
        self.restart_button = Button(self, text='RESTART', command=self.restart)

        self.adjust_widgets()

    def countdown(self):
        if self.seconds > 0:
            self.time_label.config(text=self.seconds)
            self.seconds -= 1
            self.job = self.time_label.after(1000, self.countdown)
        elif self.seconds == 0:
            self.job = None
            self.time_label.config(text='END')

    def restart(self):
        self.stop()
        self.seconds = self.TURN_SECONDS
        self.time_label.config(text=self.seconds)
        self.start()

    def stop(self):
        if self.job is not None:
            self.time_label.after_cancel(self.job)
            self.job = None

    def start(self):
        if self.job:
            return

        self.countdown()

    def adjust_widgets(self):
        self.time_label.grid(row=0, column=0, columnspan=2)

        self.start_button.grid(row=1, column=0, sticky=N+E+W+S)
        self.stop_button.grid(row=2, column=0, sticky=N+E+W+S)
        self.restart_button.grid(row=1, column=1, rowspan=2, sticky=N+E+W+S)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
