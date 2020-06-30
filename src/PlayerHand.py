from src.PokerHand import PokerHand

class PlayerHand():
    """ Playerhand takes player_hand which is a list of 7 hands with
        with player_hand[0] = None, all hands can have up to
        3 wild cards which will be resolved by determine_player_wild_cards"""

    def __init__(self, player_hand):
        self.player_hand = player_hand
        x = self.points(self.player_hand)

    def points(self, player_hand):
        """ generates points and points for all six player hands"""
        players_25card_hand = self.determine_player_wild_cards(self.player_hand)
        my_hand = PokerHand()
        self.player_hand_score = my_hand.get_six_hands_points(self.player_hand)

    def determine_player_wild_cards(self, player_hand):
        """ given player_25card_hand and player_hand (6 hands from 1 to 6
            return new player_25card_hand with WW replaced by best_wild_card"""
        # count the number of wild cards in twentyfive_cards and determine which hands they are in
        wild_cards_in_hand = 0
        wild_hand = [0, 0, 0, 0]
        wild_place = [0, 0, 0, 0]

        # find "WW" and save wild_hand and wild_place to use later
        for i in range(1, 7):
            card_place = 0
            for card in player_hand[i]:
                if card[0:2] == "WW":
                    wild_hand[wild_cards_in_hand] = i
                    wild_place[wild_cards_in_hand] = card_place
                    card_place += 1
                    wild_cards_in_hand += 1

        # if wild_cards_in_hand is >= 1, then do this
        my_hand = PokerHand()
        deck_of_cards = [s + r for s in "SHDC" for r in "23456789TJQKA"]
        if wild_cards_in_hand == 1:
            # now figure out what "card" player is using in place of wild_card
            best_wild_hand_total_score = -10000
            best_wild = []
            for wild in deck_of_cards:
                player_hand[wild_hand[0]][wild_place[0]] = wild
                wild_hand_score = my_hand.get_six_hands_points(player_hand)
                if wild_hand_score[0] > best_wild_hand_total_score:
                    best_wild_hand_total_score = wild_hand_score[0]
                    best_wild = wild
            player_hand[wild_hand[0]][wild_place[0]] = best_wild
            # print (player_hand)

        if wild_cards_in_hand == 2:
            # now figure out what "card" player is using in place of wild_card
            best_wild_hand_total_score = -10000
            best_wild = []
            for wild in deck_of_cards:
                for wild2 in deck_of_cards:
                    player_hand[wild_hand[0]][wild_place[0]] = wild
                    player_hand[wild_hand[1]][wild_place[1]] = wild2
                    wild_hand_score = my_hand.get_six_hands_points(player_hand)
                    if wild_hand_score[0] > best_wild_hand_total_score:
                        best_wild_hand_total_score = wild_hand_score[0]
                        best_wild = wild
                        best_wild2 = wild2
            player_hand[wild_hand[0]][wild_place[0]] = best_wild
            player_hand[wild_hand[1]][wild_place[1]] = best_wild2
            # print(player_hand)

        if wild_cards_in_hand == 3:
            # now figure out what "card" player is using in place of wild_card
            best_wild_hand_total_score = -10000
            best_wild = []
            for wild in deck_of_cards:
                for wild2 in deck_of_cards:
                    for wild3 in deck_of_cards:
                        player_hand[wild_hand[0]][wild_place[0]] = wild
                        player_hand[wild_hand[1]][wild_place[1]] = wild2
                        player_hand[wild_hand[2]][wild_place[2]] = wild3
                        wild_hand_score = my_hand.get_six_hands_points(player_hand)
                        if wild_hand_score[0] > best_wild_hand_total_score:
                            best_wild_hand_total_score = wild_hand_score[0]
                            best_wild = wild
                            best_wild2 = wild2
                            best_wild3 = wild3
            player_hand[wild_hand[0]][wild_place[0]] = best_wild
            player_hand[wild_hand[1]][wild_place[1]] = best_wild2
            player_hand[wild_hand[2]][wild_place[2]] = best_wild3
            # print(player_hand)
        # print ("player_hand at end", player_hand)
        return player_hand