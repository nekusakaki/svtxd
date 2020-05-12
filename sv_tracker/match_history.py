import copy


class MatchHistory:
    def __init__(self):
        self._match_history = []

    def add_match(self, clan, first, won, duration):
        self._match_history.insert(0, {'class': clan, 'first': first, 'won': won, 'duration': duration})

    def delete_match(self, match_index):
        self._match_history.pop(match_index)

    def get_matches(self):
        return copy.deepcopy(self._match_history)

    def get_match(self, match_index):
        return self._match_history[match_index].copy()

    def number_of_matches(self):
        return len(self._match_history)
