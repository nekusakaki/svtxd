class MatchStatistics:
    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.clan_wins = [0, 0, 0, 0, 0, 0, 0, 0]
        self.clan_losses = [0, 0, 0, 0, 0, 0, 0, 0]
        self.first_wins = 0
        self.first_losses = 0
        self.second_wins = 0
        self.second_losses = 0

    def total_matches(self):
        return self.wins + self.losses

    def win_percentage(self):
        if self.total_matches() == 0:
            return 0
        else:
            return self.wins / self.total_matches()

    def lose_percentage(self):
        if self.total_matches() == 0:
            return 0
        else:
            return self.losses / self.total_matches()

    def increment_wins(self, first):
        self.wins += 1
        if first:
            self.first_wins += 1
        else:
            self.second_wins += 1

    def increment_losses(self, first):
        self.losses += 1
        if first:
            self.first_losses += 1
        else:
            self.second_losses += 1

    def increment_clan_wins(self, clan):
        self.clan_wins[clan - 1] += 1

    def increment_clan_losses(self, clan):
        self.clan_losses[clan - 1] += 1

