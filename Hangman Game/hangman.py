

import random

# ----------------------------- Constants -----------------------------

WORD_LIST = ["python", "hangman", "computer", "keyboard", "monitor"]
MAX_INCORRECT_GUESSES = 6

HANGMAN_STAGES = [
    """
       ------
       |    |
       |
       |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |    |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   /
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |
    --------
    """,
]


# ----------------------------- Core Functions -----------------------------

def select_word(word_list):
    """Randomly select a word from the given list and return it in lowercase."""
    return random.choice(word_list).lower()


def format_word_progress(word, guessed_letters):
    """Return the word masked with underscores for letters not yet guessed."""
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)


def prompt_for_guess(guessed_letters):
    """
    Prompt the player for a single-letter guess and validate it.
    Re-prompts until a valid, new letter is entered.
    """
    while True:
        guess = input("Enter a letter: ").strip().lower()

        if len(guess) != 1:
            print("Invalid input: please enter exactly one letter.\n")
            continue
        if not guess.isalpha():
            print("Invalid input: please enter an alphabetic character.\n")
            continue
        if guess in guessed_letters:
            print(f"You have already guessed '{guess}'. Please choose a different letter.\n")
            continue

        return guess


def display_game_state(word, guessed_letters, incorrect_count):
    """Print the current hangman figure, word progress, and guess history."""
    print(HANGMAN_STAGES[incorrect_count])
    print(f"Word:              {format_word_progress(word, guessed_letters)}")
    print(f"Incorrect guesses: {incorrect_count} / {MAX_INCORRECT_GUESSES}")
    if guessed_letters:
        print(f"Letters guessed:   {', '.join(sorted(guessed_letters))}")
    print()


def play_round():
    """Run a single round of Hangman and return True if the player won."""
    word = select_word(WORD_LIST)
    guessed_letters = set()
    incorrect_count = 0

    print("=" * 42)
    print(" HANGMAN")
    print("=" * 42)
    print(f"The word contains {len(word)} letters.\n")

    while incorrect_count < MAX_INCORRECT_GUESSES:
        display_game_state(word, guessed_letters, incorrect_count)

        guess = prompt_for_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in word:
            print(f"Correct: '{guess}' is in the word.\n")
            if set(word) <= guessed_letters:
                display_game_state(word, guessed_letters, incorrect_count)
                print(f"You won! The word was '{word}'.")
                return True
        else:
            incorrect_count += 1
            print(f"Incorrect: '{guess}' is not in the word.\n")

    display_game_state(word, guessed_letters, incorrect_count)
    print(f"Game over. The word was '{word}'.")
    return False


def prompt_play_again():
    """Ask the player if they want to play another round; returns True/False."""
    while True:
        response = input("Play again? (y/n): ").strip().lower()
        if response in ("y", "n"):
            return response == "y"
        print("Invalid input: please enter 'y' or 'n'.")


def main():
    """Entry point: runs rounds of Hangman until the player chooses to stop."""
    wins = 0
    rounds_played = 0

    while True:
        won = play_round()
        rounds_played += 1
        wins += int(won)

        print(f"\nScore: {wins} win(s) out of {rounds_played} round(s) played.\n")

        if not prompt_play_again():
            break

    print("\nThank you for playing Hangman. Goodbye!")


if __name__ == "__main__":
    main()
