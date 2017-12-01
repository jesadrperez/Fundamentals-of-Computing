# implementation of card game - Memory
#http://www.codeskulptor.org/#user42_zgHCcdlZl4_8.py
    
import simplegui
import random

# helper function to initialize globals
def new_game():
    global deck, exposed, state, turn 
    deck = range(0,8)+range(0,8)
    random.shuffle(deck)
    exposed = [False]*16
    state = 0
    turn = 0
    label.set_text('Turns = '+str(turn))

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, state, card1, card2, turn
    
    if not exposed[pos[0]/50]:
        exposed[pos[0]/50] = True
         
        if state == 0:
            state = 1
            card1 = pos[0]/50
            turn += 1
        elif state == 1:
            state = 2
            card2 = pos[0]/50
        else:            
            if deck[card1] <> deck[card2]:
                exposed[card1] = False
                exposed[card2] = False
            state = 1   
            card1 = pos[0]/50
            turn += 1
    
    label.set_text('Turns = '+str(turn))
# cards are logically 50x100 pixels in size


def draw(canvas):
    hor = 15
    x0 = 0
    x1 = 50
    for idx in range(0,16):
        if exposed[idx]:
            canvas.draw_text(str(deck[idx]), (hor, 65), 40, 'White')
        else:
            canvas.draw_polygon([(x0,0), (x1,0), (x1,100), (x0, 100)], 1, 'Red', 'Green')
        hor += 50
        x0 = x1
        x1 += 50
    

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric