from tkinter import *


class StopwatchFrame:
    def __init__(self, master):
        self.seconds = 0
        self.duration = ''
        self.update_duration()

        self.job = None

        self.frame = Frame(master)
        self.time_label = Label(self.frame, text=self.duration, font='times 20')

        self.start_button = Button(self.frame, text='START', command=self.start)
        self.stop_button = Button(self.frame, text='STOP', command=self.stop)
        self.reset_button = Button(self.frame, text='RESET', command=self.reset)

        self.adjust_widgets()

    def update_duration(self):
        self.duration = '{:02d}'.format(int(self.seconds / 60)) + ':' + \
                        '{:02d}'.format(int(self.seconds % 60))

    def get_duration(self):
        self.stop()
        return self.seconds

    def countup(self):
        self.time_label.config(text=self.duration)
        self.seconds += 1
        self.update_duration()
        self.job = self.time_label.after(1000, self.countup)

    def reset(self):
        self.stop()
        self.seconds = 0
        self.update_duration()
        self.time_label.config(text=self.duration)

    def stop(self):
        if self.job is not None:
            self.time_label.after_cancel(self.job)
            self.job = None

    def start(self):
        if self.job:
            return

        self.countup()

    def adjust_widgets(self):
        self.time_label.grid(row=0, column=0, columnspan=2)

        self.start_button.grid(row=1, column=0, sticky=N+E+W+S)
        self.stop_button.grid(row=2, column=0, sticky=N+E+W+S)
        self.reset_button.grid(row=1, column=1, rowspan=2, sticky=N+E+W+S)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)