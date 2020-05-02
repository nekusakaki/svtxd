class MatchHistory:
    def __init__(self):
        self._match_history = []

    def add_match(self, clan, won, duration):
        self._match_history.insert(0, {'class': clan, 'won': won, 'duration': duration})

    def get_matches(self):
        return self._match_history

    def number_of_matches(self):
        return len(self._match_history)
