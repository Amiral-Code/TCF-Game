"""
Core logic for the TSF (Ten Sefirot Finder) game.

This module provides functions to generate the secret number for the game
and to calculate clues based on a player's guess compared to the secret number.
It is used by both the command-line interface (TSF_Game.py) and the GUI (tsf_gui.py).
"""
import random

def generate_secret_number(num_digits: int) -> list[str]:
    """
    Generates a secret number composed of unique random digits.

    Args:
        num_digits: The desired number of digits in the secret number.
                    Must be a positive integer between 1 and 10 (inclusive).

    Returns:
        A list of strings, where each string is a digit of the secret number.
        For example, if num_digits is 3, could return ['1', '2', '3'].

    Raises:
        ValueError: If num_digits is not a positive integer or is greater than 10.
    """
    if not isinstance(num_digits, int) or num_digits <= 0:
        raise ValueError("Number of digits must be a positive integer.")
    if num_digits > 10: # Max 10 unique digits (0-9)
        raise ValueError("Number of digits cannot exceed 10, as digits must be unique.")
    
    # Generate a sample of unique digits from 0-9
    digits = random.sample(range(10), num_digits)
    # Convert digits to strings to maintain consistency (e.g., for comparison with guesses)
    return [str(digit) for digit in digits]

def calculate_clues(guess: list[str], secret_number: list[str]) -> list[str]:
    """
    Compares the player's guess to the secret number and returns clues.

    Clue types:
    - 'T': Correct digit in the correct position.
    - 'S': Correct digit in the wrong position.
    - 'F': Incorrect digit (not in the secret number).

    Args:
        guess: A list of strings representing the player's guess.
               Example: ['1', '2', '3']
        secret_number: A list of strings representing the secret number.
                       Example: ['3', '2', '1']

    Returns:
        A list of strings representing the clues for the guess.
        Example: For guess ['1', '2', '3'] and secret_number ['3', '2', '1'],
                 returns ['S', 'T', 'S'].

    Raises:
        ValueError: If the guess or secret_number are not lists of strings,
                    or if their lengths do not match.
    """
    if not isinstance(guess, list) or not all(isinstance(d, str) for d in guess):
        raise ValueError("Guess must be a list of strings.")
    if not isinstance(secret_number, list) or not all(isinstance(d, str) for d in secret_number):
        raise ValueError("Secret number must be a list of strings.")
    if len(guess) != len(secret_number):
        raise ValueError("Guess and secret number must have the same length.")

    clues = []
    for i in range(len(guess)):
        if guess[i] == secret_number[i]:
            clues.append('T')  # Correct digit in correct position
        elif guess[i] in secret_number:
            clues.append('S')  # Correct digit in wrong position
        else:
            clues.append('F')  # Incorrect digit
    return clues
