class TrackedDeck:
    def __init__(self, deck):
        self._deck = deck
        self._card_list = deck.card_list()
        self._current_card_counts = deck.card_counts().copy()

        self._cards_left = self._deck.total_cards()

    def reset(self):
        self._current_card_counts.clear()
        self._current_card_counts = self._deck.card_counts()
        self._cards_left = self._deck.total_cards()

    def current_card_counts(self):
        return self._current_card_counts

    def card_count(self, card_id):
        return self._current_card_counts[card_id]

    def increment_card_count(self, card_id):
        if self._current_card_counts[card_id] < 3:
            self._current_card_counts[card_id] += 1
            self._cards_left += 1

    def decrement_card_count(self, card_id):
        if self._current_card_counts[card_id] > 0:
            self._current_card_counts[card_id] -= 1
            self._cards_left -= 1

    def cards_left(self):
        return self._cards_left

    def card_id_left(self, card_id):
        return self._current_card_counts[card_id]

    def draw_probability(self, card_id):
        if self._cards_left > 0:
            return self.card_id_left(card_id) / self._cards_left
        else:
            return 0

