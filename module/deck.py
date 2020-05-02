from match_statistics import MatchStatistics
from match_history import MatchHistory
import json
from urllib.request import urlopen
from card import Card
import pickle


class Deck:
    def __init__(self, name, card_ids, clan):
        self._card_ids = card_ids
        self._clan = clan
        self._stats = MatchStatistics(0, 0)
        self._history = MatchHistory()
        self._cards = []
        self._card_counts = {}
        self.name = name

    @staticmethod
    def generate_from_deck_code(name, deck_code):
        deck_code_url = "https://shadowverse-portal.com/api/v1/deck/import?format=json&deck_code=" + deck_code + "&lang=en"

        with urlopen(deck_code_url) as response:
            source = response.read()

        deck_json = json.loads(source)
        if len(deck_json['data']['errors']) == 0:
            deck_hash = deck_json['data']['hash']
            decklist_url = "https://shadowverse-portal.com/api/v1/deck?format=json&hash=" + str(deck_hash) + "&lang=en"
            with urlopen(decklist_url) as response:
                source = response.read()
            raw_json = json.loads(source)
            deck_json = raw_json['data']['deck']
            card_ids = []
            for card in deck_json['cards']:
                card_ids.append(card['card_id'])
            clan = deck_json['clan']
            return Deck(name, card_ids, clan)
        else:
            raise ValueError("Deck code does not exist.")

    @staticmethod
    def generate_from_file(file_path):
        with open(file_path, 'rb') as input_file:
            return pickle.load(input_file)

    def save_to_file(self, file_path):
        self._cards.clear()
        full_path = file_path + self.name + '.deck'
        with open(full_path, 'wb') as output_file:
            pickle.dump(self, output_file, pickle.HIGHEST_PROTOCOL)

    def rename(self, new_name):
        self.name = new_name

    def _generate_cards(self):
        self._cards.clear()
        for card_id in self._card_ids:
            self._cards.append(Card(card_id))

    def _generate_card_counts(self):
        self._card_counts.clear()
        for card_id in self._card_ids:
            if card_id in self._card_counts:
                self._card_counts[card_id] += 1
            else:
                self._card_counts[card_id] = 1

    def cards(self):
        if not self._cards:
            self._generate_cards()

        return self._cards

    def card_list(self):
        card_ids = []
        for card_id in self._card_ids:
            if card_id not in card_ids:
                card_ids.append(card_id)

        return card_ids

    def card_counts(self):
        if not self._card_counts:
            self._generate_card_counts()

        return self._card_counts

    def vials(self):
        total_vials = 0
        for card in self.cards():
            total_vials += card.vials

        return total_vials

    def clan(self):
        classes = {
            1: 'Forest',
            2: 'Sword',
            3: 'Rune',
            4: 'Dragon',
            5: 'Shadow',
            6: 'Blood',
            7: 'Haven',
            8: 'Portal'
        }
        return classes.get(self._clan)

    def win_rate(self):
        return self._stats.win_percentage() * 100.0

    def increment_wins(self, clan, duration):
        self._stats.increment_wins()
        self._stats.increment_clan_wins(clan)
        self._history.add_match(clan, True, duration)

    def increment_losses(self, clan, duration):
        self._stats.increment_losses()
        self._stats.increment_clan_losses(clan)
        self._history.add_match(clan, False, duration)

    def clan_wins(self, clan):
        return self._stats.clan_wins[clan - 1]

    def clan_losses(self, clan):
        return self._stats.clan_losses[clan - 1]

    def get_matches(self):
        return self._history.get_matches()

    def card_breakdown(self):
        card_breakdown = {'Follower': 0, 'Amulet': 0, 'Spell': 0}
        for card in self.cards():
            card_breakdown[card.get_card_type()] += 1

        return card_breakdown
