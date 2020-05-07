from tkinter import *
from tkinter import ttk
from card_image_frame import CardImageFrame
from tracked_deck import TrackedDeck


class DeckTrackerFrame:
    def __init__(self, master, deck):
        self.deck = deck
        self.tracked_deck = TrackedDeck(self.deck)

        self.frame = ttk.Frame(master)
        self.cards_frame = Frame(self.frame, padx=5, pady=5)
        self.cards = {}

        self.fill_cards_frame()
        self.adjust_widgets()

    def fill_cards_frame(self):
        card_counts = self.tracked_deck.current_card_counts()
        cards = self.deck.cards()

        for index, card_id in enumerate(card_counts):
            card = CardImageFrame(self.cards_frame, cards[card_id], card_counts[card_id])
            card.frame.grid(row=index, column=0, sticky=W + E)
            self.cards[card_id] = card

    def adjust_widgets(self):
        self.cards_frame.pack()

    def resize(self, event):
        scale = event.width / 379
        self.resize_card_images(scale)
        self.cards_frame.configure(width=event.width, height=self.cards_frame.winfo_reqheight())

    def resize_cards_frame(self, scale):
        new_width = int(self.cards_frame.winfo_reqwidth() * scale)
        self.cards_frame.configure(width=new_width)

    def resize_card_images(self, scale):
        for card_id in self.cards:
            self.cards[card_id].resize(scale)
