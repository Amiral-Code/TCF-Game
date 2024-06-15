import random
import os

def get_num_digits():
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

def get_secret_num(num_digits):
    return random.sample(range(10), num_digits)

def get_player_secret_num(num_digits):
    return get_secret_num(num_digits)

def get_bot_secret_num(num_digits):
    while True:
        bot_secret_num = input(f"Enter a secret number with {num_digits} unique digits: ")
        if len(bot_secret_num) == num_digits and bot_secret_num.isdigit() and len(set(bot_secret_num)) == num_digits:
            return list(bot_secret_num)
        else:
            print(f"Invalid input. Please enter a valid {num_digits}-digit secret number with unique digits.")

def get_guess(prompt, num_digits):
    while True:
        guess = input(prompt)
        if len(guess) == num_digits and guess.isdigit() and len(set(guess)) == num_digits:
            return list(guess)
        else:
            print(f"Invalid input. Please enter a valid {num_digits}-digit number with unique digits.")

def get_clues(guess, secret_num):
    clues = []
    for i in range(len(guess)):
        if guess[i] == secret_num[i]:
            clues.append('T')
        elif guess[i] in secret_num:
            clues.append('S')
        else:
            clues.append('F')
    return clues

def get_bot_guess(chars, bot_guess, num_digits, bot_clues, corrects, u_corrects, u_chars):
    new_bot_guess = []
    if (bot_clues.count('T') + len(corrects)) == num_digits:
        for i in range(len(bot_guess)):
            for n in chars[i]:
                if n not in u_corrects and n in u_chars:
                    chars[i].remove(n)
    for i in range(num_digits):
        valid_corrects = [item for item in corrects if item in chars[i] and item not in new_bot_guess]
        valid_chars = [item for item in chars[i] if item not in new_bot_guess]
        if bot_clues[i] == 'T':
            new_bot_guess.append(bot_guess[i])
        elif bot_clues[i] == 'S':
            new_bot_guess.append(random.choice(valid_corrects) if valid_corrects else random.choice(valid_chars))
        else:
            new_bot_guess.append(random.choice(valid_corrects) if valid_corrects else random.choice(valid_chars))
    return new_bot_guess

def update_bot_clues(chars, bot_guess, bot_secret_num, corrects, u_corrects, u_chars):
    bot_clues = []
    for i in range(len(bot_guess)):
        if bot_guess[i] not in u_chars:
            u_chars.append(bot_guess[i])
        if bot_guess[i] == bot_secret_num[i]:
            bot_clues.append('T')
            if bot_guess[i] in corrects:
                corrects.remove(bot_guess[i])
            for h in range(len(bot_guess)):
                if bot_guess[i] in chars[h]:
                    chars[h].remove(bot_guess[i])
        elif bot_guess[i] in bot_secret_num:
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

def game_setup():
    display_rules()
    num_digits = get_num_digits()
    max_guesses = get_max_guesses()
    return num_digits, max_guesses

def play_game(num_digits, max_guesses):
    num_guesses = 1
    chars = [list('0123456789') for _ in range(10)]
    corrects, u_corrects, u_chars = [], [], []
    player_secret_num = get_player_secret_num(num_digits)
    bot_secret_num = get_bot_secret_num(num_digits)
    print(f'I have thought up a {num_digits}-digit number. You have {max_guesses} guesses to get it.')
    
    bot_guess = random.sample(chars[0], num_digits)
    bot_clues = update_bot_clues(chars, bot_guess, bot_secret_num, corrects, u_corrects, u_chars)
    print(f'Bot guess #{num_guesses}: {bot_guess}')
    print(f'Bot clues #{num_guesses}: {bot_clues}\n')
    
    while num_guesses <= max_guesses:
        player_guess = get_guess(f"Enter a guess with {num_digits} unique digits #{num_guesses}: ", num_digits)
        player_clues = get_clues(player_guess, player_secret_num)
        print(f'Player guess #{num_guesses}: {player_guess}')
        print(f'Player clues #{num_guesses}: {player_clues}\n')
        
        if set(player_clues) == {'T'}:
            print('You got it!')
            return
        
        bot_guess = get_bot_guess(chars, bot_guess, num_digits, bot_clues, corrects, u_corrects, u_chars)
        bot_clues = update_bot_clues(chars, bot_guess, bot_secret_num, corrects, u_corrects, u_chars)
        print(f'Bot guess #{num_guesses + 1}: {bot_guess}')
        print(f'Bot clues #{num_guesses + 1}: {bot_clues}\n')
        
        if set(bot_clues) == {'T'}:
            print('The bot wins!')
            return
        
        num_guesses += 1
    
    print('You ran out of guesses.')
    print(f'The answer was {player_secret_num}.')

def main():
    while True:
        num_digits, max_guesses = game_setup()
        play_game(num_digits, max_guesses)
        if input('Do you want to play again? (yes or no): ').lower().startswith('n'):
            print('Thanks for playing!')
            break

if __name__ == '__main__':
    main()
