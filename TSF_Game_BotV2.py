import random
import os

def get_num_digits():
    """Get the number of digits for the secret number from the user."""
    while True:
        try:
            num_digits = int(input("How many digits do you want to be in the secret number (1-9): "))
            if 1 <= num_digits <= 9:
                return num_digits
            else:
                print("Please enter a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_max_guesses():
    """Get the maximum number of guesses from the user."""
    while True:
        try:
            max_guesses = int(input("How many guesses do you want to have (1-100): "))
            if 1 <= max_guesses <= 100:
                return max_guesses
            else:
                print("Please enter a number between 1 and 100.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def display_rules():
    """Display the rules of the game if the file exists."""
    file_path = 'TSF_Game_Rules.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            rules = file.read()

        answer = input("Do you want to see the rules of the TSF game? (yes/no): ")
        if answer.lower().startswith('y'):
            print(rules)
        else:
            print("Let's continue with the game!")
    else:
        print("Rules file not found. Continuing with the game.")

def get_bot_secret_num(num_digits):
    """Generate a random secret number with unique digits."""
    return random.sample(range(0, 10), num_digits)

def get_player_secret_num(num_digits):
    """Get the player's secret number input."""
    while True:
        player_secret_num = input(f"Enter a secret number with {num_digits} unique digits: ")
        if len(player_secret_num) != num_digits or not player_secret_num.isdigit():
            print(f"Please enter a valid {num_digits}-digit secret number.")
            continue

        unique_numbers = set(player_secret_num)
        if len(unique_numbers) != len(player_secret_num):
            print("Please make sure the digits are unique.")
            continue

        return list(player_secret_num)

def get_player_guess(num_digits, guess_num, max_guesses):
    """Get the player's guess input."""
    while guess_num <= max_guesses:
        player_guess = input(f"Enter a guess with {num_digits} unique digits (Guess #{guess_num}): ")
        if len(player_guess) != num_digits or not player_guess.isdigit():
            print(f"Please enter a valid {num_digits}-digit number.")
            continue

        unique_numbers = set(player_guess)
        if len(unique_numbers) != len(player_guess):
            print("Please make sure the digits are unique.")
            continue

        return list(player_guess)

def get_bot_guess(chars, previous_bot_guess, num_digits, bot_clues, corrects, u_corrects, u_chars):
    """Generate the bot's next guess based on the clues provided."""
    new_bot_guess = []

    if (bot_clues.count('T') + len(corrects)) == num_digits:
        for i in range(len(previous_bot_guess)):
            for n in chars[i]:
                if n not in u_corrects and n in u_chars:
                    chars[i].remove(n)

    for i in range(num_digits):
        valid_corrects = [item for item in corrects if item in chars[i] and item not in new_bot_guess]
        valid_chars = [item for item in chars[i] if item not in new_bot_guess]

        if bot_clues[i] == 'T':
            new_bot_guess.append(previous_bot_guess[i])
        else:
            new_bot_guess.append(random.choice(valid_corrects) if valid_corrects else random.choice(valid_chars))

    return new_bot_guess

def get_player_clues(player_guess, bot_secret_num):
    """Generate clues for the player's guess."""
    player_clues = []
    for i in range(len(player_guess)):
        if str(player_guess[i]) == str(bot_secret_num[i]):
            player_clues.append('T')
        elif str(player_guess[i]) in str(bot_secret_num):
            player_clues.append('S')
        else:
            player_clues.append('F')
    return player_clues

def get_bot_clues(chars, bot_guess, bot_secret_num, corrects, u_corrects, u_chars):
    """Generate clues for the bot's guess."""
    bot_clues = []
    for i in range(len(bot_guess)):
        if i not in u_chars:
            u_chars.append(bot_guess[i])
        if str(bot_guess[i]) == str(bot_secret_num[i]):
            bot_clues.append('T')
            if bot_guess[i] in corrects:
                corrects.remove(bot_guess[i])
            for h in range(len(bot_guess)):
                if bot_guess[i] in chars[h]:
                    chars[h].remove(bot_guess[i])
        elif str(bot_guess[i]) in str(bot_secret_num):
            bot_clues.append('S')
            if bot_guess[i] not in corrects:
                corrects.append(bot_guess[i])
            if bot_guess[i] not in u_corrects:
                u_corrects.append(bot_guess[i])
            if bot_guess[i] in chars[i]:
                chars[i].remove(bot_guess[i])
        else:
            bot_clues.append('F')
            for n in range(len(bot_guess)):
                if bot_guess[i] in chars[n]:
                    chars[n].remove(bot_guess[i])
    return bot_clues

def main():
    """Main function to run the game."""
    # Ask the player if they want to see the rules.
    display_rules()

    while True:
        num_digits = get_num_digits()
        max_guesses = get_max_guesses()
        guess_num = 1
        chars = [['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] for _ in range(10)]
        corrects = []
        u_corrects = []
        u_chars = []

        bot_secret_num = get_bot_secret_num(num_digits)
        player_secret_num = get_player_secret_num(num_digits)
        print(f'I have thought up a {num_digits}-digit number.')
        print(f'You have {max_guesses} guesses to get it.')
        print()

        bot_guess = random.sample(chars[0], num_digits)
        print(f'Bot guess #{guess_num}: ', bot_guess)
        bot_clues = get_bot_clues(chars, bot_guess, player_secret_num, corrects, u_corrects, u_chars)
        print(f'Bot clues #{guess_num}: ', bot_clues)
        print()

        while True:
            player_guess = get_player_guess(num_digits, guess_num, max_guesses)
            print(f'Player guess #{guess_num}: ', player_guess)

            player_clues = get_player_clues(player_guess, bot_secret_num)
            print(f'Player clues #{guess_num}: ', player_clues)
            print()
            guess_num += 1

            if set(player_clues) == {'T'}:
                print('You got it!')
                break

            bot_guess = get_bot_guess(chars, bot_guess, num_digits, bot_clues, corrects, u_corrects, u_chars)
            print(f'Bot guess #{guess_num}: ', bot_guess)
            bot_clues = get_bot_clues(chars, bot_guess, player_secret_num, corrects, u_corrects, u_chars)
            print(f'Bot clues #{guess_num}: ', bot_clues)
            print()

            if set(bot_clues) == {'T'}:
                print('The bot wins!')
                break

            if guess_num > max_guesses:
                print('You ran out of guesses.')
                print(f'The answer was {bot_secret_num}.')
                break

        if not input('Do you want to play again? (yes or no): ').lower().startswith('y'):
            print('Thanks for playing!')
            break

if __name__ == '__main__':
    main()
