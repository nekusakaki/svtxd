from sv_tracker.match_statistics import MatchStatistics
from sv_tracker.match_history import MatchHistory
import json
from urllib.request import urlopen
from sv_tracker.card import Card
import pickle
import uuid


class Deck:
    def __init__(self, name, card_ids, clan):
        self._card_ids = card_ids
        self._clan = clan
        self._stats = MatchStatistics()
        self._history = MatchHistory()
        self._cards = {}
        self._card_counts = {}
        self._card_breakdown = {}
        self._cost_breakdown = {}
        self.name = name
        self.uuid = str(uuid.uuid4().hex)[:4]

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
        file_name = self.name.replace(' ', '_') + '_' + self.uuid
        full_path = file_path + file_name + '.dck'
        with open(full_path, 'wb') as output_file:
            pickle.dump(self, output_file, pickle.HIGHEST_PROTOCOL)

    def rename(self, new_name):
        self.name = new_name

    def _generate_cards(self):
        self._cards.clear()
        for card_id in self._card_ids:
            if card_id not in self._cards.keys():
                self._cards[card_id] = Card(card_id)

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
        for card_id in self.cards():
            total_vials += self.cards()[card_id].vials * self.card_counts()[card_id]

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

    def wins(self):
        return self._stats.wins

    def losses(self):
        return self._stats.losses

    def increment_wins(self, clan, first, duration):
        self._stats.increment_wins(first)
        self._stats.increment_clan_wins(clan)
        self._history.add_match(clan, first, True, duration)

    def increment_losses(self, clan, first, duration):
        self._stats.increment_losses(first)
        self._stats.increment_clan_losses(clan)
        self._history.add_match(clan, first, False, duration)

    def wins_breakdown(self):
        return self._stats.clan_wins

    def clan_wins(self, clan):
        return self._stats.clan_wins[clan - 1]

    def losses_breakdown(self):
        return self._stats.clan_losses

    def clan_losses(self, clan):
        return self._stats.clan_losses[clan - 1]

    def first_breakdown(self):
        return [self._stats.first_wins, self._stats.first_losses]

    def second_breakdown(self):
        return [self._stats.second_wins, self._stats.second_losses]

    def get_matches(self):
        return self._history.get_matches()

    def card_breakdown(self):
        if not self._card_breakdown:
            card_breakdown = {'Follower': 0, 'Amulet': 0, 'Spell': 0}
            for card in self.cards():
                card_breakdown[card.get_card_type()] += 1

            self._card_breakdown = card_breakdown

        return self._card_breakdown

    def cost_breakdown(self):
        if not self._cost_breakdown:
            cost_breakdown = {0: [0, 0, 0], 1: [0, 0, 0], 2: [0, 0, 0], 3: [0, 0, 0], 4: [0, 0, 0],
                              5: [0, 0, 0], 6: [0, 0, 0], 7: [0, 0, 0], '8+': [0, 0, 0]}

            card_types = {'Follower': 0, 'Amulet': 1, 'Spell': 2}

            for card_id in self._card_ids:
                card = self.cards()[card_id]
                if card.cost < 8:
                    cost_breakdown[card.cost][card_types[card.get_card_type()]] += 1
                else:
                    cost_breakdown['8+'][card_types[card.get_card_type()]] += 1

            self._cost_breakdown = cost_breakdown

        return self._cost_breakdown

    def total_cards(self):
        return len(self._card_ids)
