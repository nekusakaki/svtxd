from tkinter import *
from cost_breakdown_frame import CostBreakdownFrame
from card_image_frame import CardImageFrame


class DecklistFrame:
    def __init__(self, parent, decklist):
        self._decklist = decklist
        self._frame = Frame(parent, height=500, padx=5, pady=5)
        self.deck_name_label = Label(self._frame, text=self._decklist.name, bg="black", fg="white")
        self.cards_canvas = Canvas(self._frame)
        self.cost_breakdown_frame = CostBreakdownFrame(self._frame, decklist)
        self.cards = {}

        self._fill_cards_canvas()
        self._adjust_widgets()

        self.width = 450

    def _fill_cards_canvas(self):
        card_counts = self._decklist.card_counts()
        cards = self._decklist.cards()

        for index, card_id in enumerate(card_counts):
            card = CardImageFrame(self.cards_canvas, cards[card_id], card_counts[card_id])
            card.frame.grid(row=index, column=0, sticky=W+E)
            self.cards[card_id] = card

    def _adjust_widgets(self):
        self.deck_name_label.grid(row=0, column=0, sticky=W+E+N+S)
        self.cards_canvas.grid(row=1, column=0, sticky=W+E+N+S)
        self.cards_canvas.columnconfigure(0, weight=1)
        self.cards_canvas.bind('<Configure>', self.resize)
        self.cost_breakdown_frame.frame.grid(row=2, column=0, sticky=W+E+N+S)
        self._frame.columnconfigure(0, weight=1)

    def resize(self, event):
        scale = event.width / 367
        self.resize_cards_canvas(scale)
        self.resize_card_images(scale)

    def resize_cards_canvas(self, scale):
        new_width = int(self.cards_canvas.winfo_width() * scale)
        self.cards_canvas.configure(width=new_width)

    def resize_card_images(self, scale):
        for card_id in self.cards:
            self.cards[card_id].resize(scale)

    def frame(self):
        return self._frame


