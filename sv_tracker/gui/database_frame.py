from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading
from sv_tracker.database_scripts.card_database_creator import *
from sv_tracker.database_scripts.card_image_database_creator import *


class DatabaseFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.database_thread = None

        self.help_label = Label(self, text='Requires an internet connection.' +
                                           '\nUpdate database when new expansions come out.' +
                                           '\nGenerating databases takes a long time.')
        self.card_database_label = Label(self, text='Card Database:')
        self.card_database_progress = Label(self, text='Not started')
        self.image_database_label = Label(self, text='Card Image Database:')
        self.image_database_progress = Label(self, text='Not started')

        self.generate_button = ttk.Button(self, text='Generate Databases', command=self.generate_databases)
        self.update_button = ttk.Button(self, text='Update Databases', command=self.update_databases)

        self.adjust_widgets()

    def generate_databases(self):
        self.master.grab_set()
        self.generate_button.config(state=DISABLED)
        self.update_button.config(state=DISABLED)
        confirm = messagebox.askyesno('Generate Databases.',
                                      'Are you sure you wish to generate databases?' +
                                      '\nThis takes quite a while.' +
                                      '\nUpdate database if you are not sure.')

        if confirm:
            self.database_thread = CreateDatabaseThread(self.update_card_progress_text,
                                                        self.update_image_progress_text,
                                                        self.finish)
        else:
            self.finish()

    def update_databases(self):
        self.master.grab_set()
        self.generate_button.config(state=DISABLED)
        self.update_button.config(state=DISABLED)
        self.database_thread = UpdateDatabaseThread(self.update_card_progress_text,
                                                    self.update_image_progress_text,
                                                    self.finish)

    def finish(self):
        self.master.grab_release()
        self.generate_button.config(state=NORMAL)
        self.update_button.config(state=NORMAL)

    def update_card_progress_text(self, text):
        self.card_database_progress.config(text=text)

    def update_image_progress_text(self, text):
        self.image_database_progress.config(text=text)

    def adjust_widgets(self):
        self.help_label.grid(row=0, column=0)
        self.card_database_label.grid(row=1, column=0, sticky=W)
        self.card_database_progress.grid(row=2, column=0, sticky=W+E)
        self.image_database_label.grid(row=3, column=0, sticky=W)
        self.image_database_progress.grid(row=4, column=0, sticky=W+E)
        self.generate_button.grid(row=5, column=0)
        self.update_button.grid(row=6, column=0)

        self.master.protocol('WM_DELETE_WINDOW', self.close_popup)

    def close_popup(self):
        if self.database_thread:
            if self.database_thread.isAlive():
                return

        self.master.destroy()


class UpdateDatabaseThread(threading.Thread):
    def __init__(self, card_print_function, image_print_function, finish_function):
        super().__init__(name='Database-Thread')
        self.daemon = True
        self.card_print_function = card_print_function
        self.image_print_function = image_print_function
        self.finish_function = finish_function
        self.start()

    def run(self):
        update_card_database(self.card_print_function)
        update_card_image_database(self.image_print_function)
        self.finish_function()


class CreateDatabaseThread(threading.Thread):
    def __init__(self, card_print_function, image_print_function, finish_function):
        super().__init__(name='Database-Thread')
        self.daemon = True
        self.card_print_function = card_print_function
        self.image_print_function = image_print_function
        self.finish_function = finish_function
        self.start()

    def run(self):
        create_card_database(self.card_print_function)
        create_card_image_database(self.image_print_function)
        self.finish_function()
