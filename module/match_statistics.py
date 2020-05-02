class MatchStatistics:
    def __init__(self, wins, losses):
        self.wins = wins
        self.losses = losses
        self.clan_wins = [0, 0, 0, 0, 0, 0, 0, 0]
        self.clan_losses = [0, 0, 0, 0, 0, 0, 0, 0]

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

    def increment_wins(self):
        self.wins += 1

    def increment_losses(self):
        self.losses += 1

    def increment_clan_wins(self, clan):
        self.clan_wins[clan - 1] += 1

    def increment_clan_losses(self, clan):
        self.clan_losses[clan - 1] += 1

