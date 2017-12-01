#http://www.codeskulptor.org/#user42_umEoHc2oUY_7.py

import random
import simplegui

num_range = 100
remaining = 7

def set_remaining():
    global num_range
    global remaining
    
    if num_range == 100:
        remaining = 7
    else:
        remaining = 10

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    global guess
    global num_range
    global remaining
    
    set_remaining()
    secret_number = random.randrange(0, num_range)
    
    print ''
    print "New Game Started!"
    print "  Range Set to", str(num_range)+'.'
    print "  You have", str(remaining), "guesses remaining."
    # remove this when you add your code
    #pass


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game
    global num_range
    global remaining
    
    remaining = 7
    num_range = 100
    new_game()
    
    # remove this when you add your code
    #pass

def range1000():
    # button that changes the range to [0,1000) and starts a new game
    global num_range
    global remaining
    
    remaining = 10
    num_range = 1000
    new_game()
    
    #pass
    
def input_guess(guess):
    # main game logic goes here
    global secret_number
    global remaining
    
    remaining -= 1
    print "  Guess was", guess
    guess = int(guess)
    
    if guess == secret_number:
        print "****You Win!****"
        new_game()
    elif guess > secret_number:
        print "  Guess Lower"
        print "  You have", str(remaining), "guesses remaining."
    else:
        print "  Guess Higher"
        print "  You have", str(remaining), "guesses remaining."
    
    if remaining == 0:
        print "  Secret Number was", str(secret_number)
        print "****You Lose!****"
        new_game()
    
    # remove this when you add your code
    #pass

    
# create frame
frame = simplegui.create_frame('Guessing game', 200, 200)
frame.add_button('New Game', new_game, 100)
frame.add_button('Range is [0,100)', range100, 100)
frame.add_button('Range is [0,1000)', range1000, 100)
frame.add_input('Guess:', input_guess, 50)

# register event handlers for control elements and start frame
frame.start()


# call new_game
new_game()


# always remember to check your completed program against the grading rubric
