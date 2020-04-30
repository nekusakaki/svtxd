
class MatchStatistics:
    win = 0
    losses = 0

    def __init__(self, wins, losses):
        self.wins = wins
        self.losses = losses

    def total_matches(self):
        return self.wins + self.losses

    def win_percentage(self):
        return self.wins / self.total_matches()

    def lose_percentage(self):
        return self.losses / self.total_matches()



