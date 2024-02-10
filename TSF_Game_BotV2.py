import random
import os


def get_num_digits():
    while True:
        try:
            num_digits = int(input("How many digits do you want to be in the secret number: "))
            if 1 <= num_digits <= 9:
                return num_digits
            else:
                print("Please enter a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_max_guesses():
    while True:
        try:
            max_guesses = int(input("How many guesses do you want to have: "))
            if 1 <= max_guesses <= 100:
                return max_guesses
            else:
                print("Please enter a number between 1 and 100.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def display_rules():
    file_path = 'CLASS\TSF_Game_Rules.txt'

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

def get_player_secret_num(num_digits):
    secret_num = random.sample(range(0, 9), num_digits)
    return secret_num

def get_bot_secret_num(num_digits):
    while True:
        bot_secret_num = input(f"Enter a secret number with {num_digits} unique numbers: ")

        if len(bot_secret_num) != num_digits or not bot_secret_num.isdigit():
            print(f"Please enter a valid {num_digits}-digit secret number.")
            continue

        unique_numbers = set(bot_secret_num)
        if len(unique_numbers) != len(bot_secret_num):
            print("Please make sure the numbers are unique.")
            continue

        return list(bot_secret_num)

def get_player_guess(num_digits, num_guesses, max_guesses):
    while num_guesses <= max_guesses:
        player_guess = input(f"Enter a guess with {num_digits} unique numbers: #{num_guesses} ")

        if len(player_guess) != num_digits or not player_guess.isdigit():
            print(f"Please enter a valid {num_digits}-digit number.")
            continue

        unique_numbers = set(player_guess)
        if len(unique_numbers) != len(player_guess):
            print("Please make sure the numbers are unique.")
            continue

        return list(player_guess)

def get_bot_guess(chars, bot_guess, num_digits, bot_clues, corrects, u_corrects, u_chars):
    new_bot_guess = []

    if (bot_clues.count('T') + len(corrects)) == 4:
        for i in range(len(bot_guess)):
            for n in chars[i]:
                if n not in u_corrects and n in u_chars :
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

def get_player_clues(player_guess, bot_secret_num):
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
    bot_clues = []
    for i in range(len(bot_guess)):
        #print(bot_guess[i])
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
    # Ask the player if he wants to see the rules.
    display_rules()

    while True:
        num_digits = get_num_digits()
        max_guesses = get_max_guesses()
        num_guesses = 1
        chars = [['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                ]
        corrects = []
        u_corrects = []
        u_chars = []
        player_secret_num = get_player_secret_num(num_digits)
        bot_secret_num = get_bot_secret_num(num_digits)
        print(f'I have thought up a {num_digits} digit number.')
        print(f'You have {max_guesses} guesses to get it.')
        print()
        

        
        bot_guess = random.sample(chars[0], num_digits)
        print(f'Bot guess #{num_guesses}: ', bot_guess)
        bot_clues = get_bot_clues(chars, bot_guess, bot_secret_num, corrects, u_corrects, u_chars)
        print(f'Bot clues #{num_guesses}: ', bot_clues)
        print()

        while True:
            player_guess = get_player_guess(num_digits, num_guesses, max_guesses)
            print(f'Player guess #{num_guesses}: ', str(player_guess))
            
            player_clues = get_player_clues(player_guess, player_secret_num)
            print(f'Player clues #{num_guesses}: ', player_clues)
            print()
            num_guesses += 1

            if set(player_clues) == {'T'}:
                print('You got it!')
                break

            bot_guess = get_bot_guess(chars, bot_guess, num_digits, bot_clues, corrects, u_corrects, u_chars)
            print(f'Bot guess #{num_guesses}: ', bot_guess)
            bot_clues = get_bot_clues(chars, bot_guess, bot_secret_num, corrects, u_corrects, u_chars)
            print(f'Bot clues #{num_guesses}: ', bot_clues)
            print()

            if set(bot_clues) == {'T'}:
                print('The bot win!')
                break

            if num_guesses > max_guesses:
                print('You ran out of guesses.')
                print(f'The answer was {player_secret_num}.')
                break

        print('Do you want to play again? (yes or no)')
        if not input('> ').lower().startswith('y'):
            print('Thanks for playing!')
            break

if __name__ == '__main__':
    main()
