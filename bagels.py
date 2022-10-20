"""TCF, by Amiral7YT 
A deductive logic game where you must guess a number based on clues.
This code is available at https://
Tags: short, game, puzzle"""

import random

NUM_DIGITS = 4  # (!) Try setting this to 1 or 10.
MAX_GUESSES = 10  # (!) Try setting this to 1 or 100.


def main():
    print('''TCF, a deductive logic game.
By Amiral7YT

I am thinking of a {}-digit number with no repeated digits.
Try to guess what it is. Here are some clues:
When I say: That means:
     T      That digit is correct and in the right position.
     C      That digit is correct but in the wrong position.
     F      That digit is incorrect.

For example, if the secret number was 2485 and your guess was 8436, the
clues would be ['F', 'T', 'C', 'F'].'''.format(NUM_DIGITS))

    while True:  # Main game loop.
        # This stores the secret number the player needs to guess:
        secretNum = random.sample(range(0, 9), 4)
        print('I have thought up a {} digit number.'.format(NUM_DIGITS))
        print(' You have {} guesses to get it.'.format(MAX_GUESSES))

        numGuesses = 1
        while numGuesses <= MAX_GUESSES:
            guess = [ ]
            # Keep looping until they enter a valid guess:
            while len(guess) != NUM_DIGITS :
                print('Guess #{}: '.format(numGuesses))
                while len(guess) != NUM_DIGITS :
                    guess = input('Guess > ')
                    if len(guess) != NUM_DIGITS :
                        guess = input('Guess > ')
                    elif len(guess) == NUM_DIGITS:
                        guess = [int(x) for i,x in enumerate(guess)]
                        #Make sure there is no reapeted numbers
                        dup = [ ]
                        for i in guess :                           
                            if i not in dup :
                                dup.append(i)
                            else:
                                dup.clear()
                                guess = input('Guess > ')
                guess = [int(x) for i,x in enumerate(guess)]
            clues = getClues(guess, secretNum)
            print(clues)
            numGuesses += 1

            if clues == ['T', 'T', 'T', 'T']:
                print('You got it!')
                break  # They're correct, so break out of this loop.
            if numGuesses > MAX_GUESSES:
                print('You ran out of guesses.')
                print('The answer was {}.'.format(secretNum))

        # Ask player if they want to play again.
        print('Do you want to play again? (yes or no)')
        if not input('> ').lower().startswith('y'):
            break
    print('Thanks for playing!')


def getClues(guess, secretNum):
    
    clues = [ ]

    for i in range(len(guess)):
        if guess[i] == secretNum[i]:
            # A correct digit is in the correct place.
            clues.append('T')
        elif guess[i] in secretNum:
            # A correct digit is in the incorrect place.
            clues.append('C')
        else :
            clues.append('F')     
    # Make a single string from the list of string clues.
    return clues
    """Returns a string with the (T)rue, (C)hange, (F)alse clues for guess
    and secret number pair."""
    if clues == ['T', 'T', 'T', 'T']:
        print('You got it!')
        return
    

# If the program is run (instead of imported), run the game:
if __name__ == '__main__':
    main()
