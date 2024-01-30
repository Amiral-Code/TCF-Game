import random

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
    with open('TSF_Game_Rules.txt', 'r') as file:
        rules = file.read()

    answer = input("Do you want to see the rules of the TSF game? (yes/no): ")

    if answer.lower().startswith('y'):
        print(rules)
    else:
        print("Let's continue with the game!")

def get_secret_num(num_digits):
    secret_num = random.sample(range(0, 9), num_digits)
    return secret_num

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

def get_clues(player_guess, secret_num):
    clues = []
    for i in range(len(player_guess)):
        if str(player_guess[i]) == str(secret_num[i]):
            clues.append('T')
        elif str(player_guess[i]) in str(secret_num):
            clues.append('S') 
        else:
            clues.append('F')
    return clues

def main():
    # Ask the player if he want to see the rules.
    display_rules()
    while True:
        num_digits = get_num_digits()
        max_guesses = get_max_guesses()

        secret_num = get_secret_num(num_digits)
        print(f'I have thought up a {num_digits} digit number.')
        print(f'You have {max_guesses} guesses to get it.')
        num_guesses = 1

        while True:
            player_guess = get_player_guess(num_digits, num_guesses, max_guesses)
            print(str(player_guess))
            num_guesses += 1

            clues = get_clues(player_guess, secret_num)
            print(clues)

            if set(clues) == {'T'}:
                print('You got it!')
                break

            if num_guesses > max_guesses:
                print('You ran out of guesses.')
                print(f'The answer was {secret_num}.')
                break

        print('Do you want to play again? (yes or no)')
        if not input('> ').lower().startswith('y'):
            print('Thanks for playing!')
            break

if __name__ == '__main__':
    main()
