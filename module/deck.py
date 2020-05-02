from match_statistics import MatchStatistics
import json
from urllib.request import urlopen
from card import Card


class Deck:
    def __init__(self, name, card_ids, clan):
        self._card_ids = card_ids
        self._clan = clan
        self._stats = MatchStatistics(0, 0)
        self._cards = []
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

    def rename(self, new_name):
        self.name = new_name

    def _generate_cards(self):
        self._cards = []
        for card_id in self._card_ids:
            self._cards.append(Card(card_id))

    def cards(self):
        if not self._cards:
            self._generate_cards()

        return self._cards

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

    def increment_wins(self):
        self._stats.increment_wins()

    def increment_losses(self):
        self._stats.increment_losses()

    def clan_wins(self):
        return self._stats.clan_wins

    def increment_clan_wins(self, clan):
        self._stats.increment_clan_wins(clan)

    def clan_losses(self):
        return self._stats.clan_losses

    def increment_clan_losses(self, clan):
        self._stats.increment_clan_losses(clan)