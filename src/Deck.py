""" Deck is Class to create deck cards and deal cards to players
    :parameter
    num_players (int): Number of players
    num_cards (int): Number of cards dealt per player
    num_decks (int): Number of "53 card decks (1 wild card)" to use
    :return
    player_hands (list): list of hands
    example: Deck(6,25,3) -> 6 players, 25 cards, 3 decks
"""

from random import shuffle
import logging
logging.basicConfig(filename='pyramid_poker.log',level=logging.WARNING)

class Deck:
    def __init__(self, num_players=6, num_cards=25, num_decks=3):
        self.num_players = num_players
        self.num_cards = num_cards
        self.num_decks = num_decks
        self.player_hands = [[] for i in range(num_players)]
        suit = 'SHDC'
        rank = 'AKQJT98765432'
        deck_symbol = '+-*=^'
        cards_needed = self.num_players * self.num_cards
        if num_decks * 53 < cards_needed:
            self.num_decks = cards_needed//53 + 1
            if self.num_decks > len(deck_symbol):
                print ("Error, needs more than 5 decks")
        deck_symbol = '+-*=^'[:self.num_decks]
        self.deck = [s + r + d for s in suit for r in rank for d in deck_symbol]
        self.deck.extend(["WW+", "WW-", "WW*", "WW=", "WW^"][:self.num_decks]) # add wild cards

    def deal(self):
        for i in range(10):
            shuffle(self.deck)
        logging.debug (self.deck)
        for i in range(self.num_players):
            pyramid_poker_list = self.deck[i::self.num_players]
            self.player_hands[i] = pyramid_poker_list[:self.num_cards]
            logging.debug ('{0} {1}'.format(i, self.player_hands[i]))
        return (self.player_hands)