# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 500
wager = 100

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

    def draw_back(self, canvas, pos):
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.number_of_cards = 0
        self.hand_value = 0

    def __str__(self):
        return str(self.cards)

    def add_card(self, card):
        self.cards.append(card)
        self.number_of_cards += 1
        
    def get_value(self):
        self.hand_value = 0
        for card in self.cards:
            if card[1] == "A":
                self.hand_value += 11
            elif card[1] == "T":
                self.hand_value += 10
            elif card[1] == "Q":
                self.hand_value += 10
            elif card[1] == "K":
                self.hand_value += 10
            elif card[1] == "J":
                self.hand_value += 10
            else:
                self.hand_value += int(card[1])
        return self.hand_value
 
    def reset_hand(self):
        self.cards = []

# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        self.top_card = 1
        self.create_deck()
        
    def shuffle(self):
        random.shuffle(self.cards)

    def reshuffle(self):
        self.cards = []
        self.create_deck()
        self.top_card = 1
        self.shuffle()
        
    def create_deck(self):
        for i in SUITS:
            for j in RANKS:
                self.cards.insert(0, [str(i), str(j)])
        
    def deal_card(self):
        self.top_card += 1
        if self.top_card > 40:
            print "deck is done"
            self.reshuffle()
        return self.cards.pop(1)

    def __str__(self):
        return str(self.cards) + str(self.top_card)
    
    def return_card(self, card_number):
        return self.cards[card_number]

    def return_suit(self, card_number):
        i = 0
        for card in self.cards:
            if i == card_number:
                return card[0]
            else:
                i += 1

#define event handlers for buttons
def deal():
    global outcome, in_play, score, wager

    # check if player reset cards before end of turn
    if in_play:
        score -= wager
    
    player_hand.reset_hand()
    dealer_hand.reset_hand()

    # deal two cards to player
    next_card = d1.deal_card()
    player_hand.add_card(next_card)

    next_card = d1.deal_card()
    player_hand.add_card(next_card)

    # deal two cards to dealer
    next_card = d1.deal_card()
    dealer_hand.add_card(next_card)
    
    in_play = True

def hit():
    global in_play, score, wager
    
    # if the hand is in play, hit the player
    if in_play:
        next_card = d1.deal_card()
        player_hand.add_card(next_card)

        # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            in_play = False
            next_card = d1.deal_card()
            dealer_hand.add_card(next_card)
            score -= wager
        
def stand():
    global in_play, score, wager

    if in_play:
        next_card = d1.deal_card()
        dealer_hand.add_card(next_card)
    
        # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() < 17:
            next_card = d1.deal_card()
            dealer_hand.add_card(next_card)

        if dealer_hand.get_value() < 17:
            next_card = d1.deal_card()
            dealer_hand.add_card(next_card)

        if dealer_hand.get_value() > 21:
            score += wager
        elif dealer_hand.get_value() > player_hand.get_value():
            score -= wager
        elif dealer_hand.get_value() < player_hand.get_value():
            score += wager
            
        in_play = False   
        
# draw handler    
def draw(canvas):
    global in_play, score
    
    # this draws dealer cards
    x = 100
    for card in dealer_hand.cards:
        card = Card(card[0], card[1])
        card.draw(canvas, [x, 100])
        x += 80

    if x == 180:
        for card in dealer_hand.cards:
            card = Card(card[0], card[1])
            card.draw_back(canvas, [180, 100])
    
    # this draws player cards
    x = 100
    for card in player_hand.cards:
        card = Card(card[0], card[1])
        card.draw(canvas, [x, 400])
        x += 80

    # this draws the titles    
    canvas.draw_text("Blackjack", [200, 60], 50, "White")
#    canvas.draw_text("Dealer Hand " + str(dealer_hand.get_value()), [150, 60], 50, "Black")    
    canvas.draw_text("Player Count " + str(player_hand.get_value()), [150, 360], 50, "Black")

    # this determines the outcome of the game and presents a message    
    if dealer_hand.get_value() == 0:
        canvas.draw_text("Press Deal to Begin", [100, 260], 30, "Black")
    elif in_play:
        canvas.draw_text("Press Hit or Stand", [100, 260], 30, "Black")
    elif player_hand.get_value() > 21:
        canvas.draw_text("Player Busted! Press Deal to Play Again", [100, 260], 30, "Black")
    elif dealer_hand.get_value() > 21:
        canvas.draw_text("Dealer Busted! Press Deal to Play Again", [100, 260], 30, "Black")
    elif player_hand.get_value() == dealer_hand.get_value():
        canvas.draw_text("Tie Hand - No Winner", [100, 260], 30, "Black")
    elif player_hand.get_value() > dealer_hand.get_value():
        canvas.draw_text("Player Wins! Press Deal to Play Again", [100, 260], 30, "Black")
    else:
        canvas.draw_text("Dealer Wins! Press Deal to Play Again", [100, 260], 30, "Black")

    # this prints the current score
    canvas.draw_text("Player Money = $" + str(score), [100, 560], 40, "Black")
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
frame.start()

player_hand = Hand()
dealer_hand = Hand()
d1 = Deck()
d1.shuffle()

