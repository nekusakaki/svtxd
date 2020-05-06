from deck import Deck


deck = Deck.generate_from_file('../decks/49bf32c9ad8a4d819ddd868ca28e3969.dck')

for i in range(1, 9):
    for j in range(i):
        deck.increment_wins(i, 300)


print(deck.wins_breakdown())

deck.save_to_file('../decks/')