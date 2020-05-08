from tkinter import *
from tkinter import ttk
from gui.card_image_frame import CardImageFrame
from tracked_deck import TrackedDeck
from gui.turn_timer_frame import TurnTimerFrame
from gui.stop_watch_frame import StopwatchFrame
from gui.change_count_frame import ChangeCountFrame
from gui.log_match_frame import LogMatchFrame


class DeckTrackerFrame:
    def __init__(self, master, deck, refresh_function):
        self.deck = deck
        self.tracked_deck = TrackedDeck(self.deck)
        self.function = refresh_function

        self.frame = Frame(master, pady=5)
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
