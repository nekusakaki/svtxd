from tkinter import *
from tkinter import ttk
from card_image_frame import CardImageFrame
from tracked_deck import TrackedDeck
from turn_timer_frame import TurnTimerFrame
from stop_watch_frame import StopwatchFrame


class DeckTrackerFrame:
    def __init__(self, master, deck, refresh_function):
        self.deck = deck
        self.tracked_deck = TrackedDeck(self.deck)
        self.function = refresh_function

        self.frame = ttk.Frame(master)
        self.cards_frame = Frame(self.frame, padx=5, pady=0)
        self.cards = {}
        self.counter_buttons = {}

        self.stop_watch_frame = StopwatchFrame(self.frame)
        self.turn_timer_frame = TurnTimerFrame(self.frame)

        self.reset_button = ttk.Button(self.frame, text='RESET CARDS', command=self.reset)

        self.log_match_window = None
        self.log_match_frame = None
        self.log_match_button = ttk.Button(self.frame, text='Log Match', command=self.log_match_popup)

        self.fill_cards_frame()
        self.adjust_widgets()

    def log_match_popup(self):
        self.log_match_window = Toplevel()
        self.log_match_window.transient(self.frame)

        self.log_match_frame = LogMatchFrame(self.log_match_window, self.stop_watch_frame, self.log_match)
        self.log_match_frame.frame.pack()

    def log_match(self, win, clan, first, duration):
        if win:
            self.deck.increment_wins(clan, first, duration)
        else:
            self.deck.increment_losses(clan, first, duration)
        self.deck.save_to_file('../decks/')

        self.function()
        self.log_match_window.destroy()

    def reset(self):
        self.tracked_deck.reset()
        for card_id in self.cards:
            self.cards[card_id].update_count(self.tracked_deck.card_count(card_id))

    def fill_cards_frame(self):
        card_counts = self.tracked_deck.current_card_counts()
        cards = self.deck.cards()

        for index, card_id in enumerate(card_counts):
            card = CardImageFrame(self.cards_frame, cards[card_id], card_counts[card_id])
            card.frame.grid(row=index, column=0, sticky=W + E)
            self.cards[card_id] = card

            counter_button = ChangeCountFrame(self.cards_frame, card_id,
                                              self.increment_card, self.decrement_card)
            counter_button.frame.grid(row=index, column=1, sticky=N+S)
            self.counter_buttons[card_id] = counter_button

    def increment_card(self, card_id):
        self.tracked_deck.increment_card_count(card_id)
        self.cards[card_id].update_count(self.tracked_deck.card_count(card_id))

    def decrement_card(self, card_id):
        self.tracked_deck.decrement_card_count(card_id)
        self.cards[card_id].update_count(self.tracked_deck.card_count(card_id))

    def adjust_widgets(self):
        self.reset_button.grid(row=0, column=0, sticky=W, padx=5)
        self.cards_frame.grid(row=1, column=0, columnspan=2)

        self.stop_watch_frame.frame.grid(row=2, column=0, padx=5, pady=5, sticky=N+E+W+S)
        self.turn_timer_frame.frame.grid(row=2, column=1, rowspan=2, padx=5, pady=5, sticky=N+E+W+S)

        self.log_match_button.grid(row=3, column=0, sticky=N+E+W+S, padx=5)

    def resize(self, event):
        scale = event.width / 480
        self.resize_card_images(scale)
        self.resize_counter_buttons(scale)
        self.cards_frame.configure(width=event.width, height=self.cards_frame.winfo_reqheight())

    def resize_card_images(self, scale):
        for card_id in self.cards:
            self.cards[card_id].resize(scale)

    def resize_counter_buttons(self, scale):
        for card_id in self.cards:
            self.counter_buttons[card_id].resize(scale)


class ChangeCountFrame:
    def __init__(self, master, card_id, inc_function, dec_function):
        self.card_id = card_id
        self.inc_function = inc_function
        self.dec_function = dec_function

        self.frame = Frame(master)
        self.inc_button = Button(self.frame, text='+', width=3, height=1,
                                 command=self.increment_count, bg='green')
        self.dec_button = Button(self.frame, text='-', width=3, height=1,
                                 command=self.decrement_count, bg='red')

        self.adjust_widgets()

    def increment_count(self):
        self.inc_function(self.card_id)

    def decrement_count(self):
        self.dec_function(self.card_id)

    def resize(self, scale):
        new_width = int(round(4 * scale))
        new_height = int(round(2 * scale))
        self.inc_button.configure(width=new_width, height=new_height)
        self.dec_button.configure(width=new_width, height=new_height)

    def adjust_widgets(self):
        self.inc_button.pack(side=LEFT)
        self.dec_button.pack(side=LEFT)


class LogMatchFrame:
    def __init__(self, master, stopwatch, log_function):
        self.frame = Frame(master)
        self.stopwatch = stopwatch
        self.function = log_function

        self.won_label = Label(self.frame, text='Won?')
        self.won = BooleanVar()
        self.won.set(True)
        self.win = Radiobutton(self.frame, text='Win', variable=self.won, value=True)
        self.lose = Radiobutton(self.frame, text='Lose', variable=self.won, value=False)

        self.first_label = Label(self.frame, text='First?')
        self.is_first = BooleanVar()
        self.is_first.set(True)
        self.first = Radiobutton(self.frame, text='First', variable=self.is_first, value=True)
        self.second = Radiobutton(self.frame, text='Second', variable=self.is_first, value=False)

        self.against_label = Label(self.frame, text='Against?')
        self.clan = IntVar()
        self.clan.set(1)
        self.clan_frame = Frame(self.frame)
        self.forest = Radiobutton(self.clan_frame, text='Forest', variable=self.clan, value=1)
        self.sword = Radiobutton(self.clan_frame, text='Sword', variable=self.clan, value=2)
        self.rune = Radiobutton(self.clan_frame, text='Rune', variable=self.clan, value=3)
        self.dragon = Radiobutton(self.clan_frame, text='Dragon', variable=self.clan, value=4)
        self.shadow = Radiobutton(self.clan_frame, text='Shadow', variable=self.clan, value=5)
        self.blood = Radiobutton(self.clan_frame, text='Blood', variable=self.clan, value=6)
        self.haven = Radiobutton(self.clan_frame, text='Haven', variable=self.clan, value=7)
        self.portal = Radiobutton(self.clan_frame, text='Portal', variable=self.clan, value=8)

        self.duration = self.stopwatch.get_duration()
        self.duration_label = Label(self.frame,
                                    text='Duration: {:02d}:{:02d}'.format(int(self.duration / 60),
                                                                          int(self.duration % 60)))

        self.log_button = ttk.Button(self.frame, text='Log', command=self.log)

        self.adjust_widgets()

    def log(self):
        self.function(self.won.get(), self.clan.get(), self.is_first.get(), self.duration)

    def adjust_widgets(self):
        self.won_label.grid(row=0, column=0, columnspan=2, pady=5)
        self.win.grid(row=1, column=0)
        self.lose.grid(row=1, column=1)

        self.first_label.grid(row=2, column=0, columnspan=2, pady=5)
        self.first.grid(row=3, column=0)
        self.second.grid(row=3, column=1)

        self.against_label.grid(row=4, column=0, columnspan=2, pady=5)
        self.clan_frame.grid(row=5, column=0, columnspan=2)

        self.forest.grid(row=0, column=0)
        self.sword.grid(row=0, column=1)
        self.rune.grid(row=0, column=2)
        self.dragon.grid(row=0, column=3)
        self.shadow.grid(row=1, column=0)
        self.blood.grid(row=1, column=1)
        self.haven.grid(row=1, column=2)
        self.portal.grid(row=1, column=3)

        self.duration_label.grid(row=6, column=0, columnspan=2, sticky=N+E+W+S, pady=5)

        self.log_button.grid(row=7, column=0, columnspan=2, sticky=N+E+W+S, padx=5, pady=5)
