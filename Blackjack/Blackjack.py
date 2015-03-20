# Mini-project #6 - Blackjack

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
outcome = ""

score = 0

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
        for i in range(5):
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    
    
    def draw_back(self, canvas, pos):
        # if the card is claps or spade, take the blue back image
        if self.suit == 'C' or self.suit == 'S':
            card_loc = (CARD_CENTER[0], 
                        CARD_CENTER[1])
            canvas.draw_image(card_back, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
        # if the card is claps or spade, take the red back image
        elif self.suit == 'H' or self.suit == 'D':
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0], 
                        CARD_CENTER[1] )
            canvas.draw_image(card_back, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
    
        
# define hand class
class Hand:
    def __init__(self):
        self.hand_cards = []
        # create Hand object

    def __str__(self):
        hand = ""	# return a string representation of a hand
        for card in self.hand_cards:
            hand += str(card)
            hand += " " 
        return "hand Contains : " + hand
        
    def add_card(self, card):
        self.hand_cards.append(card)
            # add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_value = 0
        ace_count = 0
        card_count = 0
        for card in self.hand_cards:
            card_count += 1
            hand_value += VALUES[str(card)[-1]]
            if card.rank == "A":
                ace_count += 1
        if ace_count == 0:
            return hand_value
        else:
            if (hand_value + 10) <= 21:
                return (hand_value + 10)
            else:
                return hand_value

    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.hand_cards:
            card.draw(canvas, pos)
            pos[0] += 90
        
    def draw_back(self, canvas, pos):
        for i in range(1):
            for card in self.hand_cards:
                card.draw_back(canvas, pos)
            
 
    
        
# define deck class 
        
class Deck:
    # create a Deck object
    def __init__(self):
        self.deck_cards =[]	
        for suits in SUITS:
            for rank in RANKS:
                c = Card (suits, rank)
                self.deck_cards.append(c)
                

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck_cards)    

    def deal_card(self):
        # deal a card object from the deck
        card = random.choice(self.deck_cards)
        self.deck_cards.remove(card)
        return card
    
    def __str__(self):
        # return a string representing the deck
        deck = "" 
        for card in self.deck_cards:
            deck += str(card)
            deck += " "
        return "Deck Contains : " + deck


#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, my_deck, score, result, outcome

    # your code goes here
    my_deck = Deck()
    my_deck.shuffle()
    result = ""
    # If player press deal in the middle of a game he will loose that game
    if in_play == True:
        result = "You lose. New Game started"
        #outcome = "New deal?"
        score -= 1
        
    #else:
    player_hand = Hand()
    dealer_hand = Hand()
    
    # initializing outcome message
    
    outcome = 'Hit or stand ? '
     
    for i in range(2):
        player_hand.add_card(my_deck.deal_card())
        dealer_hand.add_card(my_deck.deal_card())
        
    #print "Player " + str(player_hand)
    #print "Dealer " + str(dealer_hand)    
    in_play = True

def hit():
    global player_hand, my_deck, in_play, score, result, outcome
    # if the hand is in play, hit the player
    result = ""
    if in_play == True:
        if player_hand.get_value() <= 21:
            player_hand.add_card(my_deck.deal_card())
            # if busted, assign a message to outcome, update in_play and score
            if player_hand.get_value() > 21:
                result = "You went bust and lose"
                outcome = "New deal?"
                in_play = False
                score -= 1
       
def stand():
    global dealer_hand, my_deck, in_play, score, result, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    result = ""
    if in_play == True:
        if player_hand.get_value() > 21:
            # assign a message to outcome, update in_play and score
            result = "You went bust and lose."
            outcome = "New deal?"
            in_play = False
            # print "Dealer " + str(dealer_hand)
            score -= 1
        else:
            while(dealer_hand.get_value() < 17):
                dealer_hand.add_card(my_deck.deal_card())
                # print updated dealer_hand
            if dealer_hand.get_value() > 21:
                result = "Dealer is busted. You win"
                outcome = "New deal?"
                score += 1
                in_play = False
                
    # Decide who wins
            elif player_hand.get_value() <= dealer_hand.get_value():
                result = "You lose"
                outcome = "New deal?"
                score -= 1
                in_play = False
            else:
                result = "You win"
                outcome = "New deal?"
                score += 1
                in_play = False	

                
# draw handler    
def draw(canvas):
    global outcome
    
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("BLACJACK", (150, 50), 60, 'Blue')
    canvas.draw_text("Score : " + str(score), (420, 100), 35, 'Red')
    canvas.draw_text("Dealer", (40, 160), 35, 'Purple')
    canvas.draw_text(result, (180, 160), 35, 'White')
    canvas.draw_text("Player", (40, 350), 35, 'Black')
    canvas.draw_text(outcome, (180, 350), 35, 'White')
    
    #draw the cards in a hand
    dealer_hand.draw(canvas, [40, 190])
    player_hand.draw(canvas, [40, 380])
    
    # Flip the first card
    if in_play == True:
        dealer_hand.draw_back(canvas, [40, 190])
        
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])


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


# remember to review the gradic rubric