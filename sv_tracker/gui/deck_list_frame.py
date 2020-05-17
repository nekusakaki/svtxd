from tkinter import *
from PIL import ImageTk
from sv_tracker.class_icons import ClassIcons
from sv_tracker.gui.graphs.cost_breakdown_frame import CostBreakdownFrame
from sv_tracker.gui.card_image_frame import CardImageFrame


class DeckListFrame(Frame):
    def __init__(self, master, deck):
        self.deck = deck
        self.height = 500
        super().__init__(master, padx=5, pady=5)

        self.class_icon = ClassIcons().get_icon(self.deck.clan())
        self.resized_image = self.class_icon.resize((50, 50))
        self.tk_image = ImageTk.PhotoImage(self.resized_image)
        self.deck_name_label = self._generate_deck_name_label(self)

        self.cards_canvas = Canvas(self, width=300)
        self.cards_frame = Frame(self.cards_canvas, height=1000, bd=0)
        self.vbar = Scrollbar(self, orient=VERTICAL)
        self.cost_breakdown_frame = CostBreakdownFrame(self, deck)
        self.cards = {}

        self._fill_cards_frame()
        self._adjust_widgets()

    def _generate_deck_name_label(self, master):
        label = Label(master, image=self.tk_image, text=self.deck.name, bg="black", fg="white",
                      compound=RIGHT, anchor=E, font="Sans 12 bold")
        return label

    def _fill_cards_frame(self):
        card_counts = self.deck.card_counts()
        cards = self.deck.cards()

        for index, card_id in enumerate(card_counts):
            card = CardImageFrame(self.cards_frame, cards[card_id], card_counts[card_id])
            card.grid(row=index, column=0, sticky=W+E)
            self.cards[card_id] = card

    def _adjust_widgets(self):
        self.deck_name_label.grid(row=0, column=0, columnspan=2, sticky=W+E+N+S)

        self.vbar.grid(row=1, column=1, sticky=N+S)
        self.vbar.configure(command=self.cards_canvas.yview)

        self.cards_canvas.grid(row=1, column=0, sticky=W+E+N+S, pady=5)
        self.cards_canvas.create_window((0, 0), window=self.cards_frame, anchor=N+W)
        self.cards_canvas.configure(yscrollcommand=self.vbar.set)
        self.cards_canvas.bind('<Enter>', self.bind_mousewheel)
        self.cards_canvas.bind('<Leave>', self.unbind_mousewheel)
        self.cards_canvas.bind('<Configure>', self.resize)

        self.cost_breakdown_frame.frame.grid(row=2, column=0, columnspan=2, sticky=W+E+N+S)

        self.columnconfigure(0, weight=1)

    def bind_mousewheel(self, event):
        self.cards_canvas.bind_all('<MouseWheel>', self.on_mousewheel)

    def unbind_mousewheel(self, event):
        self.cards_canvas.unbind_all('<MouseWheel>')

    def on_mousewheel(self, event):
        self.cards_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def resize(self, event):
        scale = event.width / 385
        self.resize_card_images(scale)
        self.cards_frame.configure(width=event.width, height=self.cards_frame.winfo_reqheight())
        canvas_height = self.height - \
                        (self.deck_name_label.winfo_height() + self.cost_breakdown_frame.frame.winfo_height()) - \
                        24
        self.cards_canvas.configure(height=canvas_height)
        self.resize_cards_canvas(scale)

    def resize_cards_frame(self, scale):
        new_width = int(self.cards_frame.winfo_reqwidth() * scale)
        self.cards_frame.configure(width=new_width)

    def resize_cards_canvas(self, scale):
        self.cards_canvas.configure(scrollregion=self.cards_canvas.bbox('all'))

    def resize_card_images(self, scale):
        for card_id in self.cards:
            self.cards[card_id].resize(scale)

    def destroy(self):
        self.cost_breakdown_frame.destroy()
        super().destroy()
