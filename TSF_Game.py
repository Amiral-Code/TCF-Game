import random # random is no longer needed for core logic, but keeping for now if other parts use it.
from core_game_logic import generate_secret_number, calculate_clues
from bots import BotPlayer # Import BotPlayer

def get_num_digits():
    while True:
        try:
            num_digits_str = input("Enter the number of digits for the secret number (1-9): ")
            if not num_digits_str.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            num_digits = int(num_digits_str)
            if 1 <= num_digits <= 9:
                return num_digits
            else:
                print("Please enter a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_max_guesses():
    while True:
        try:
            max_guesses_str = input("Enter the maximum number of guesses (1-100): ")
            if not max_guesses_str.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            max_guesses = int(max_guesses_str)
            if 1 <= max_guesses <= 100:
                return max_guesses
            else:
                print("Please enter a number between 1 and 100.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def display_rules():
    try:
        with open('TSF_Game_Rules.txt', 'r') as file:
            rules = file.read()
        
        answer = input("Do you want to see the rules of the TSF game? (yes/no): ")
        if answer.lower().startswith('y'):
            print(rules)
        else:
            print("\nLet's continue with the game!")
    except FileNotFoundError:
        print("TSF_Game_Rules.txt not found. Cannot display rules.")
    except Exception as e:
        print(f"Error reading rules: {e}")

def get_player_guess(num_digits: int, current_guess_num: int) -> list[str]:
    while True:
        player_guess_str = input(f"Enter your guess #{current_guess_num} ({num_digits} unique digits): ")
        if len(player_guess_str) != num_digits:
            print(f"Error: Guess must have {num_digits} digits.")
            continue
        if not player_guess_str.isdigit():
            print("Error: Guess must contain only digits.")
            continue
        if len(set(player_guess_str)) != num_digits:
            print("Error: Digits in guess must be unique.")
            continue
        return list(player_guess_str)

def get_clues_from_player(num_digits: int, bot_guess_str: str) -> list[str]:
    """Prompts the human player for clues for the bot's guess and validates them."""
    while True:
        clue_input = input(f"Enter clues for bot's guess '{bot_guess_str}' (e.g., TSF, {num_digits} characters): ").upper()
        if len(clue_input) != num_digits:
            print(f"Error: Clues must be {num_digits} characters long.")
            continue
        if not all(c in 'TSF' for c in clue_input):
            print("Error: Clues can only contain 'T', 'S', or 'F'.")
            continue
        return list(clue_input)

def play_human_guesses_mode():
    print("\n--- Mode: You Guess Computer's Number ---")
    num_digits = get_num_digits()
    max_guesses = get_max_guesses()

    try:
        secret_num_list = generate_secret_number(num_digits)
    except ValueError as e:
        print(f"Error setting up game: {e}")
        return 

    print(f'\nI have thought up a {num_digits}-digit number.')
    print(f'You have {max_guesses} guesses to get it.')
    # print(f"Hint (for debugging): The secret number is {''.join(secret_num_list)}")

    num_guesses_taken = 0
    game_won = False

    while num_guesses_taken < max_guesses:
        num_guesses_taken += 1
        player_guess_list = get_player_guess(num_digits, num_guesses_taken)

        try:
            clues = calculate_clues(player_guess_list, secret_num_list)
        except ValueError as e:
            print(f"Error calculating clues: {e}. Please try your guess again.")
            num_guesses_taken -= 1 
            continue

        clues_str_display = " ".join(clues)
        print(f"Clues: {clues_str_display}")

        if all(c == 'T' for c in clues):
            print('Congratulations! You got it!')
            game_won = True
            break
    
    if not game_won:
        print('\nYou ran out of guesses.')
        print(f"The answer was {''.join(secret_num_list)}.")

def play_bot_guesses_mode():
    print("\n--- Mode: Bot Guesses Your Number ---")
    num_digits = get_num_digits()
    max_guesses = get_max_guesses()

    print(f"\nOkay, think of a {num_digits}-digit number with unique digits.")
    input("Press Enter when you have your number and are ready for the bot to start guessing...")

    bot = BotPlayer(num_digits)
    bot_guesses_taken = 0
    bot_won = False

    while bot_guesses_taken < max_guesses:
        bot_guesses_taken += 1
        bot_guess_list = bot.generate_guess()
        bot_guess_str = "".join(bot_guess_list)
        
        print(f"\nBot's guess #{bot_guesses_taken}: {bot_guess_str}")
        
        player_clues_list = get_clues_from_player(num_digits, bot_guess_str)
        
        bot.update_strategy(bot_guess_list, player_clues_list)

        if all(c == 'T' for c in player_clues_list):
            print(f"\nBot guessed your number '{bot_guess_str}' in {bot_guesses_taken} tries! Well done, Bot!")
            bot_won = True
            break
    
    if not bot_won:
        print(f"\nBot ran out of guesses after {max_guesses} tries. You stumped the bot!")

def main():
    display_rules()
    while True:
        print("\nChoose a game mode:")
        print("1. You guess the computer's number")
        print("2. Bot guesses your number")
        print("3. Exit")
        
        mode_choice = input("Enter your choice (1, 2, or 3): ")

        if mode_choice == '1':
            play_human_guesses_mode()
        elif mode_choice == '2':
            play_bot_guesses_mode()
        elif mode_choice == '3':
            print("Thanks for playing TSF Game!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

        play_again = input('\nDo you want to play another game or switch modes? (yes or no): ')
        if not play_again.lower().startswith('y'):
            print('Thanks for playing TSF Game!')
            break

if __name__ == '__main__':
    main()
