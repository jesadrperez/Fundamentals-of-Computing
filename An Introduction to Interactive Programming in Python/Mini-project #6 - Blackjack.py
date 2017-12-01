# Mini-project #6 - Blackjack
#http://www.codeskulptor.org/#user42_yUWSsWhf55_12.py

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "Test"
score = [0, 0]

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
class Hand:
    def __init__(self):
        self.cards = [] # create Hand object

    def __str__(self):
        s = 'There are ' + str(len(self.cards)) + ' cards in the hand: '
        for card in self.cards:
            s += str(card) + ' ' 
        return s	# return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        
        NumAces = 0
        total = 0
        
        for card in self.cards:
            if (card.get_rank() == 'A'):
                total += 11
                NumAces += 1
            else:
                total += VALUES[card.get_rank()]                
                
        while NumAces > 0:
            if total > 21:
                total -= 10
            NumAces -= 1
        return total    
   
    def draw(self, canvas, pos):
        row1 = 0
        row2 = 0
        for card in self.cards:
            if row1 < 6:
                card.draw(canvas, [pos[0]+row1*CARD_SIZE[0], pos[1]])
            else:
                card.draw(canvas, [pos[0]+row2*CARD_SIZE[0], 
                                   pos[1]+CARD_SIZE[1]])
                row2 += 1
            row1 += 1
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []	
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.cards.append(card)

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        card = self.cards[-1]
        self.cards.pop(-1)
        return card            
    
    def __str__(self):
        # return a string representing the deck
        s = 'Deck contains ' + str(len(self.cards)) + " cards: "
        for card in self.cards:
            s += str(card) + ' ' 
        return s	# return a string representation of a hand           

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand
    
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    dealer_hand = Hand()
    
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())   
   
    if in_play:
        score[1] += 1
        outcome = 'You lose!'

    in_play = True
    outcome = "Hit or stand?"
    
def hit():
    global in_play, outcome, score
     
    # if the hand is in play, hit the player
    if in_play and (player_hand.get_value() < 22):
        player_hand.add_card(deck.deal_card())
        if (player_hand.get_value() > 21):
            outcome = 'You busted! New deal?'
            in_play = False
            score[1] += 1
            
def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global in_play, outcome, score   
    
    print ''
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card()) 
        if dealer_hand.get_value() > 21:
            outcome = 'Dealer busted! New deal?'
            score[0] += 1
        else:
            if dealer_hand.get_value() < player_hand.get_value():
                outcome = 'You won! New deal?'
                score[0] += 1
            else:
                outcome = 'You lose! New deal?'
                score[1] += 1
        in_play = False                
    else:
        outcome = 'You busted! New Deal?'
        score[1] += 1
    
# draw handler    
def draw(canvas):
    dealer_hand.draw(canvas, [CARD_SIZE[0], 0])
    player_hand.draw(canvas, [CARD_SIZE[0], 400])
    
    idx = 0    
    for letter in 'BLACKJACK':
        if idx < 5:
            canvas.draw_text(letter, (5, 75+idx*60), 75, 'Black')
        else:
            canvas.draw_text(letter, (5, 75+idx*60), 75, 'Red')
        idx += 1
        
    canvas.draw_text(outcome, (75, 300), 50, 'Black')
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                      (CARD_BACK_CENTER[0]+CARD_SIZE[0], CARD_BACK_CENTER[1]), CARD_BACK_SIZE)
        
    canvas.draw_text('Won: '+ str(score[0]), (500, 450), 30, 'Black')
    canvas.draw_text('Lost: '+ str(score[1]), (500, 480), 30, 'Black')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()