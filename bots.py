"""
TSF Game - Bot Player Logic

This module defines the `BotPlayer` class, which encapsulates the logic and
strategy for an AI player in the TSF (Ten Sefirot Finder) game.
The bot maintains a knowledge base derived from clues received on its guesses
and uses this knowledge to generate subsequent, more informed guesses.
This bot is designed to be used in the "Bot Guesses Your Number" mode of TSF_Game.py.
"""
import random

class BotPlayer:
    """
    Represents an AI player for the TSF game.

    The bot attempts to guess a secret multi-digit number based on clues ('T', 'S', 'F')
    it receives for its previous guesses. It maintains an internal state representing
    its current knowledge about the secret number.

    Attributes:
        num_digits (int): The number of digits in the secret number.
        all_possible_digits (list[str]): A list of all possible digits ('0' through '9').
        possible_digits_per_position (list[set[str]]): For each position in the secret number,
            a set of digits that could potentially be in that position.
        known_correct_misplaced (set[str]): A set of digits known to be in the secret
            number but whose correct position has not yet been determined.
        confirmed_digits_at_position (list[str | None]): A list where each index represents
            a position in the secret number. If a digit is confirmed for a position,
            it's stored as a string at that index; otherwise, None.
        eliminated_digits (set[str]): A set of digits known not to be in the secret number at all.
        last_guess (list[str]): The most recent guess made by the bot.
    """
    def __init__(self, num_digits: int):
        """
        Initializes the BotPlayer.

        Args:
            num_digits: The number of unique digits in the secret number the bot will try to guess.
        """
        self.num_digits: int = num_digits
        self.all_possible_digits: list[str] = [str(i) for i in range(10)]
        
        # --- Bot's Knowledge Base Initialization ---
        # For each position, initially all digits are possible.
        self.possible_digits_per_position: list[set[str]] = [set(self.all_possible_digits) for _ in range(num_digits)]
        
        # Digits known to be in the number but not in the right place yet.
        self.known_correct_misplaced: set[str] = set()
        
        # Digits confirmed to be at a specific position. `None` means unknown.
        self.confirmed_digits_at_position: list[str | None] = [None] * num_digits
        
        # Digits confirmed NOT to be in the number at all.
        self.eliminated_digits: set[str] = set()

        self.last_guess: list[str] = [] # Stores the last guess made by the bot for reference.

    def generate_guess(self) -> list[str]:
        """
        Generates the bot's next guess based on its current knowledge.
        The strategy involves several steps:
        1. Fill in any digits already confirmed for specific positions.
        2. Attempt to place digits known to be correct but misplaced ('S' clues)
           into plausible remaining slots.
        3. Fill any remaining slots with digits that are still possible for those
           positions, ensuring uniqueness and avoiding eliminated digits.
        4. Includes fallback mechanisms for complex or constrained scenarios.

        Returns:
            A list of strings representing the bot's guess.
            Example: ['1', '2', '3']
        """
        guess: list[str | None] = [None] * self.num_digits
        used_digits_in_current_guess: set[str] = set()

        # Step 1: Fill in confirmed digits
        for i in range(self.num_digits):
            if self.confirmed_digits_at_position[i] is not None:
                guess[i] = self.confirmed_digits_at_position[i]
                used_digits_in_current_guess.add(guess[i])

        # Step 2: Try to use known_correct_misplaced digits in new, valid positions
        # Shuffle to introduce some randomness if multiple misplaced digits could fit.
        available_misplaced = list(self.known_correct_misplaced - used_digits_in_current_guess)
        random.shuffle(available_misplaced)

        for i in range(self.num_digits):
            if guess[i] is None: # If position not yet filled by a confirmed digit
                for digit in available_misplaced:
                    # Check if this misplaced digit is possible at this position and not already used in this guess
                    if digit in self.possible_digits_per_position[i] and digit not in used_digits_in_current_guess:
                        guess[i] = digit
                        used_digits_in_current_guess.add(digit)
                        break # Digit placed, move to the next position in the guess

        # Step 3: Fill remaining slots with other possible digits
        for i in range(self.num_digits):
            if guess[i] is None: # If position still not filled
                # Candidates are those possible for this position, not yet used in this guess, and not globally eliminated.
                candidates = list(
                    self.possible_digits_per_position[i] - 
                    used_digits_in_current_guess - 
                    self.eliminated_digits
                )
                random.shuffle(candidates) # Randomize choice among valid candidates
                
                if candidates:
                    guess[i] = candidates[0]
                    used_digits_in_current_guess.add(guess[i])
                else:
                    # Fallback strategy: If no candidates from position-specific list,
                    # try any digit not yet used and not eliminated.
                    # This can happen if initial assumptions or clue interpretations were too restrictive.
                    fallback_candidates = list(set(self.all_possible_digits) - used_digits_in_current_guess - self.eliminated_digits)
                    random.shuffle(fallback_candidates)
                    if fallback_candidates:
                        guess[i] = fallback_candidates[0]
                        used_digits_in_current_guess.add(guess[i])
                    else:
                        # This is a critical state, implying a contradiction or that all digits are somehow accounted for or eliminated.
                        # This should be extremely rare with num_digits <= 10.
                        # For robustness, assign a placeholder or raise an error.
                        # Current behavior: print warning and use a random available digit, which might violate some constraint.
                        print(f"Warning: Bot in critical state at generate_guess. Position {i}, Used: {used_digits_in_current_guess}, Eliminated: {self.eliminated_digits}")
                        remaining_options = [d for d in self.all_possible_digits if d not in used_digits_in_current_guess]
                        if remaining_options:
                             guess[i] = random.choice(remaining_options)
                             used_digits_in_current_guess.add(guess[i])
                        else: # Should ideally not be reached if num_digits <= 10
                             guess[i] = '?' # Placeholder for error

        # Final check: Ensure all elements in guess are strings and the guess has unique digits.
        # The logic above should strive for this, but this is a safeguard.
        current_guess_set = {g for g in guess if g is not None and g != '?'}
        if len(current_guess_set) != self.num_digits or any(g is None or g == '?' for g in guess):
            # Attempt to fill Nones or '?' with unique digits not yet used.
            # This is a more robust fallback for ensuring guess length and uniqueness.
            final_fill_digits = list(set(self.all_possible_digits) - current_guess_set - self.eliminated_digits)
            random.shuffle(final_fill_digits)
            for i in range(self.num_digits):
                if guess[i] is None or guess[i] == '?':
                    if final_fill_digits:
                        new_digit = final_fill_digits.pop(0)
                        guess[i] = new_digit
                        current_guess_set.add(new_digit) # Keep track of used digits for this final fill
                    else:
                        # If still can't fill, indicates a severe issue with bot's state or constraints.
                        print(f"CRITICAL ERROR: Bot cannot form a complete unique guess of length {self.num_digits}. Current constructed guess: {guess}")
                        guess[i] = random.choice(list(set(self.all_possible_digits) - current_guess_set)) if set(self.all_possible_digits) - current_guess_set else 'X' # Last resort placeholder

        self.last_guess = [str(g) for g in guess] # Ensure all elements are strings
        return self.last_guess


    def update_strategy(self, guess: list[str], clues: list[str]):
        """
        Updates the bot's knowledge base based on the last guess and the clues received.

        Args:
            guess: The bot's last guess (list of strings).
            clues: The clues received for that guess (list of strings: 'T', 'S', 'F').
                   'T' = Correct digit, correct position.
                   'S' = Correct digit, wrong position.
                   'F' = Incorrect digit (not in the secret number).
        """
        if len(guess) != self.num_digits or len(clues) != self.num_digits:
            # print(f"Error: Bot received guess/clues length mismatch. Guess: {len(guess)}, Clues: {len(clues)}, Expected: {self.num_digits}")
            return # Or raise an error

        for i in range(self.num_digits):
            digit_in_guess = guess[i]
            clue_for_digit = clues[i]

            if clue_for_digit == 'T':
                # Digit is confirmed at this position
                self.confirmed_digits_at_position[i] = digit_in_guess
                self.possible_digits_per_position[i] = {digit_in_guess} # Only this digit is possible here
                self.known_correct_misplaced.discard(digit_in_guess) # No longer just 'misplaced'
                self.eliminated_digits.discard(digit_in_guess) # Cannot be eliminated if it's 'T'
                
                # Remove this confirmed digit from possibilities of all OTHER positions
                for j in range(self.num_digits):
                    if i != j:
                        self.possible_digits_per_position[j].discard(digit_in_guess)

            elif clue_for_digit == 'S':
                # Digit is in the number, but NOT at this position
                self.known_correct_misplaced.add(digit_in_guess)
                self.possible_digits_per_position[i].discard(digit_in_guess) # Cannot be at this position
                self.eliminated_digits.discard(digit_in_guess) # Cannot be eliminated if it's 'S'

            elif clue_for_digit == 'F':
                # Digit is not in the secret number at all
                self.eliminated_digits.add(digit_in_guess)
                self.known_correct_misplaced.discard(digit_in_guess) # Cannot be misplaced if it's not in number
                # Remove from all positions' possibilities
                for j in range(self.num_digits):
                    self.possible_digits_per_position[j].discard(digit_in_guess)

        # --- Post-clue processing refinements ---

        # 1. Ensure consistency: if a digit is confirmed, it's not misplaced.
        for confirmed_digit in self.confirmed_digits_at_position:
            if confirmed_digit is not None:
                self.known_correct_misplaced.discard(confirmed_digit)

        # 2. If a digit is eliminated, ensure it's removed from all position possibilities.
        # (This is often handled by 'F' logic but serves as a good safeguard).
        for elim_digit in self.eliminated_digits:
            for i in range(self.num_digits):
                self.possible_digits_per_position[i].discard(elim_digit)
        
        # 3. Deduction: If a 'known_correct_misplaced' digit can only fit in one remaining
        #    unconfirmed slot (based on `possible_digits_per_position`), then confirm it there.
        non_confirmed_indices = [k for k, d_val in enumerate(self.confirmed_digits_at_position) if d_val is None]
        
        # Iterate multiple times or until no new deductions are made in a pass,
        # as one deduction can lead to others. For simplicity, one pass here,
        # but a loop `while new_deductions_made:` would be more robust.
        made_deduction_in_pass = True 
        while made_deduction_in_pass:
            made_deduction_in_pass = False
            for m_digit in list(self.known_correct_misplaced): # Iterate over a copy as set might change
                possible_placements_for_m_digit = []
                for idx in non_confirmed_indices:
                    if self.confirmed_digits_at_position[idx] is None and \
                       m_digit in self.possible_digits_per_position[idx]:
                        possible_placements_for_m_digit.append(idx)
                
                if len(possible_placements_for_m_digit) == 1:
                    idx_to_confirm = possible_placements_for_m_digit[0]
                    # print(f"Bot deduction: Digit {m_digit} must be at position {idx_to_confirm}")
                    self.confirmed_digits_at_position[idx_to_confirm] = m_digit
                    self.possible_digits_per_position[idx_to_confirm] = {m_digit}
                    self.known_correct_misplaced.discard(m_digit) # Now confirmed
                    
                    # This digit is now confirmed, remove it from other non-confirmed positions' possibilities
                    for j_idx in non_confirmed_indices:
                        if j_idx != idx_to_confirm:
                            self.possible_digits_per_position[j_idx].discard(m_digit)
                    
                    non_confirmed_indices.remove(idx_to_confirm) # This index is now confirmed
                    made_deduction_in_pass = True # Signal that a deduction was made, loop again

    def get_bot_state_for_debugging(self) -> dict:
        """ Helper method to get the bot's internal state for debugging. """
        return {
            "num_digits": self.num_digits,
            "possible_digits_per_position": [sorted(list(s)) for s in self.possible_digits_per_position], # Sets to sorted lists
            "known_correct_misplaced": sorted(list(self.known_correct_misplaced)),
            "confirmed_digits_at_position": self.confirmed_digits_at_position,
            "eliminated_digits": sorted(list(self.eliminated_digits)),
            "last_guess": self.last_guess
        }

# Example Usage (for testing the bot class directly if this script is run)
if __name__ == '__main__':
    test_num_digits = 4
    bot = BotPlayer(test_num_digits)
    print("Initial Bot State:", bot.get_bot_state_for_debugging())

    # --- Simulate a few rounds of guessing and updating strategy ---
    # Example Scenario: Secret Number is ['1', '2', '3', '4']
    
    # Round 1
    guess1 = bot.generate_guess() # Bot makes a guess
    print(f"\nRound 1: Bot's guess: {guess1}")
    # Simulate human providing clues for guess1 against secret ['1', '2', '3', '4']
    # This part would normally be done by calling core_game_logic.calculate_clues
    # E.g., if guess1 = ['0', '5', '1', '2'], clues1 = ['F', 'F', 'S', 'S']
    clues1 = ['F', 'F', 'S', 'S'] # Example clues if guess1 was ['0','5','1','2']
    print(f"Clues for guess1: {clues1}")
    bot.update_strategy(guess1, clues1)
    print("Bot state after guess 1:", bot.get_bot_state_for_debugging())

    # Round 2
    guess2 = bot.generate_guess()
    print(f"\nRound 2: Bot's guess: {guess2}")
    # E.g., if guess2 = ['1', '3', '8', '9'] vs secret ['1', '2', '3', '4']
    # clues2 = ['T', 'S', 'F', 'F']
    clues2 = ['T', 'S', 'F', 'F'] # Example
    print(f"Clues for guess2: {clues2}")
    bot.update_strategy(guess2, clues2)
    print("Bot state after guess 2:", bot.get_bot_state_for_debugging())

    # Round 3
    guess3 = bot.generate_guess()
    print(f"\nRound 3: Bot's guess: {guess3}")
    # ... and so on
    # E.g., if guess3 = ['1', '2', '4', '3'] vs secret ['1', '2', '3', '4']
    # clues3 = ['T', 'T', 'S', 'S']
    clues3 = ['T','T','S','S']
    print(f"Clues for guess3: {clues3}")
    bot.update_strategy(guess3, clues3)
    print("Bot state after guess 3:", bot.get_bot_state_for_debugging())

    # Round 4
    guess4 = bot.generate_guess()
    print(f"\nRound 4: Bot's guess: {guess4}")
    clues4 = ['T','T','T','T'] # Assuming it gets it right
    print(f"Clues for guess4: {clues4}")
    bot.update_strategy(guess4, clues4)
    print("Bot state after guess 4:", bot.get_bot_state_for_debugging())
    if all(c == 'T' for c in clues4):
        print("\nBot successfully guessed the number!")
