from deck import Deck
from random import random


deck = Deck.generate_from_file('../decks/d8d4f8487d634629aea2da2800e8c5e3.dck')

for i in range(1, 9):
    for j in range(5):
        random_number = random()
        coin_flip = random() > 0.5

        if random_number <= 0.56:
            deck.increment_wins(i, coin_flip, 300)
        else:
            deck.increment_losses(i, coin_flip, 300)


print(deck.wins_breakdown())

deck.save_to_file('../decks/')