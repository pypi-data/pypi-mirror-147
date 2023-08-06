class Guess:
    def __init__(self, guess: str = "") -> None:
        self.guess = guess

    def guess_score(guess: str, solution: str) -> list[dict]:
        # Score player guess by assigning colour to letter/position
        guess_score = []
        for idx, letter in enumerate(guess):
            if letter not in solution:
                guess_score.append({letter: "blue"})  # Not in word
            elif guess[idx] == solution[idx]:
                guess_score.append({letter: "green"})  # Correct spot
            else:
                guess_score.append({letter: "yellow"})  # In word but wrong spot

        return guess_score
