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
                                           '\nUpdate database when new expansions come out' +
                                           '\nor balance changes happen.')
        self.card_database_label = Label(self, text='Card Database:')
        self.card_database_progress = Label(self, text='Not started')
        self.image_database_label = Label(self, text='Card Image Database:')
        self.image_database_progress = Label(self, text='Not started')

        self.balance_changes_button = ttk.Button(self, text='Balance Changes', command=self.balance_changes)
        self.new_expansion_button = ttk.Button(self, text='New Expansion', command=self.new_expansion)
        self.missing_databases_button = ttk.Button(self, text='Missing Databases', command=self.missing_databases)

        self.adjust_widgets()

    def balance_changes(self):
        self.start()
        confirm = messagebox.askyesno('Balance Changes.',
                                      'Are you sure you wish to generate databases for a balance change?' +
                                      '\nThis takes a while.')

        if confirm:
            self.database_thread = BalanceChangesThread(self.update_card_progress_text,
                                                        self.update_image_progress_text,
                                                        self.finish)
        else:
            self.finish()

    def new_expansion(self):
        self.start()
        confirm = messagebox.askyesno('New Expansion.',
                                      'Are you sure you wish to generate databases for a new expansion?' +
                                      '\nThis takes a while.')

        if confirm:
            self.database_thread = NewExpansionThread(self.update_card_progress_text,
                                                      self.update_image_progress_text,
                                                      self.finish)
        else:
            self.finish()

    def missing_databases(self):
        self.start()
        confirm = messagebox.askyesno('Missing Databases.',
                                      'Are you sure you wish to generate databases?' +
                                      '\nThis takes a while.')

        if confirm:
            self.database_thread = MissingDatabasesThread(self.update_card_progress_text,
                                                          self.update_image_progress_text,
                                                          self.finish)
        else:
            self.finish()

    def start(self):
        self.master.grab_set()
        self.balance_changes_button.config(state=DISABLED)
        self.new_expansion_button.config(state=DISABLED)
        self.missing_databases_button.config(state=DISABLED)

    def finish(self):
        self.master.grab_release()
        self.balance_changes_button.config(state=NORMAL)
        self.new_expansion_button.config(state=NORMAL)
        self.missing_databases_button.config(state=NORMAL)

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
        self.balance_changes_button.grid(row=5, column=0)
        self.new_expansion_button.grid(row=6, column=0)
        self.missing_databases_button.grid(row=7, column=0)

        self.master.protocol('WM_DELETE_WINDOW', self.close_popup)

    def close_popup(self):
        if self.database_thread:
            if self.database_thread.isAlive():
                return

        self.master.destroy()


class BalanceChangesThread(threading.Thread):
    def __init__(self, card_print_function, image_print_function, finish_function):
        super().__init__(name='Database-Thread')
        self.daemon = True
        self.card_print_function = card_print_function
        self.image_print_function = image_print_function
        self.finish_function = finish_function
        self.start()

    def run(self):
        create_card_database(self.card_print_function)
        update_card_image_database(self.image_print_function)
        self.finish_function()


class NewExpansionThread(threading.Thread):
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


class MissingDatabasesThread(threading.Thread):
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
