import random
import sys

from pythle import cli
from pythle.load_wordlist import load_wordlist
from pythle.player_stats import PlayerStats

WORDS = load_wordlist("words.txt")
SOLUTIONS = load_wordlist("solutions.txt")

MAX_GUESSES = 6


def main():
    player_stats = PlayerStats()

    while True:  # Main game loop
        solution: str = random.choice(SOLUTIONS)  # Set new solution
        guesses: list[str] = []  # Reset player guesses

        cli.display_title_art()
        cli.display_player_stats(player_stats)

        while len(guesses) < MAX_GUESSES:  # Loop for each player guess
            guess = cli.get_player_guess(guesses, MAX_GUESSES, WORDS)
            if guess.upper() in ["Q", "QUIT"]:
                cli.goodbye_message()
                sys.exit()  # Quit
            else:
                guesses.append(guess)
                cli.display_all_guess_scores(guesses, solution)
                if guess == solution:
                    cli.win_message()
                    player_stats.games_played += 1
                    player_stats.wins += 1
                    player_stats.win_streak += 1
                    break
                if len(guesses) == MAX_GUESSES:
                    cli.lose_message(solution)
                    player_stats.games_played += 1
                    player_stats.win_streak = 0

        player_continue = cli.get_player_continue()
        if player_continue is False:
            cli.goodbye_message()
            sys.exit()  # Quit


if __name__ == "__main__":
    main()
