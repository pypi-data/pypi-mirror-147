import os
import platform

from pythle.guess import Guess
from pythle.player_stats import PlayerStats

""" DISPLAY SCORE COLOURS """

if platform.system() == "Windows":
    # enables ANSI colors in Windows terminal
    os.system("color")

ansi_colours = {"green": "42", "yellow": "43", "blue": "44"}


def display_guess_score(guess_score: list[dict]) -> None:
    # Print the guess scores to the terminal, adding colout with ansi escape characters
    for letter_score in guess_score:
        for letter, colour in letter_score.items():
            print(f"\033[{ansi_colours[colour]}m {letter} \033[0;0m", end="")


def display_all_guess_scores(guesses: list[str], solution: str) -> None:
    # Print all guess scores to the terminal
    for guess in guesses:
        display_guess_score(Guess.guess_score(guess, solution))
        print("")  # Adds new line between guess score


""" GET PLAYER INPUTS """


def get_player_guess(
    guesses: list[str],
    max_guesses: int,
    word_list: list[str],
) -> str:
    # Validates the player input from the user
    while True:
        print(f"Enter your guess ({len(guesses) + 1} / {max_guesses}), or 'Q' to quit.")
        guess = input()
        guess = guess.upper()
        if guess != "Q" and guess not in word_list:
            print("Each guess must be a valid five-letter word.")
        else:
            return guess


def get_player_continue() -> bool:
    while True:
        print("Play again? Enter 'Y' to continue or 'N' to quit.")
        player_continue = input()
        player_continue = player_continue.upper()
        if player_continue in ["N", "NO"]:
            return False
        if player_continue in ["Y", "YES"]:
            return True


""" DISPLAY STATISTICS """


def display_player_stats(player_stats: PlayerStats) -> None:
    print(
        f"""
====================================
            STATISTICS
        {player_stats.games_played} Played, {player_stats.win_ratio()}% Wins
        Current Streak is {player_stats.win_streak}
====================================
"""
    )


""" OTHER MESSAGES """


def display_title_art() -> None:
    print(
        """
 _____ __ __ _____ _____ __    _____
|  _  |  |  |_   _|  |  |  |  |   __|
|   __|_   _| | | |     |  |__|   __|
|__|    |_|   |_| |__|__|_____|_____|"""
    )


def goodbye_message() -> None:
    print("Thanks for playing!\n")


def win_message() -> None:
    print("\nYou win!\n")


def lose_message(solution: str) -> None:
    print(f"\nYou lose! The Wordle was {solution}.\n")
