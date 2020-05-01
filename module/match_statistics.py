class MatchStatistics:
    def __init__(self, wins, losses):
        self.wins = wins
        self.losses = losses

    def total_matches(self):
        return self.wins + self.losses

    def win_percentage(self):
        if self.total_matches() == 0:
            return 0
        else:
            return self.wins / self.total_matches()

    def lose_percentage(self):
        if self.total_matches() ==0:
            return 0
        else:
            return self.losses / self.total_matches()


stats = MatchStatistics(0, 0)


print(stats.win_percentage())

