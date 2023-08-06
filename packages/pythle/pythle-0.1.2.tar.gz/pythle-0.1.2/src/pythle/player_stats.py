from dataclasses import dataclass


@dataclass
class PlayerStats:
    games_played: int = 0
    wins: int = 0
    win_streak: int = 0

    def win_ratio(self) -> int:
        if self.games_played == 0:
            win_ratio = 0
        else:
            win_ratio = round((self.wins / self.games_played) * 100)
        return win_ratio