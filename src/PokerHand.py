from enum import Enum
from src.Analysis import *
from src.ReadProbability import *
from src.CumulativeLearning import *
from src.sort_cards import *
from src.get_dir import get_dir
# from src.WriteProb import *
import pickle

ranks = "W123456789TJQKA"
suits = "WCDHS"
first = True

class HandType(Enum):
    TenK = 20
    TenSF = 19
    NineK = 18
    NineSF = 17
    EightK = 16
    EightSF = 15
    SevenK = 14
    SevenSF = 13
    SixK = 12
    SixSF = 11
    FiveK = 10
    FiveSF = 9
    FourK = 8
    FullH = 7
    Flush = 6
    Straight = 5
    Trip = 4
    TwoP = 3
    OneP = 2
    HighC = 1

class PokerHand():
    """ represents a n-card hand - calculates various attributes """
    def __init__(self, hand = ["SA+"]):
        """ initializes object with hand, suit_rank_array, hand_type
        hand_type_value and hand_score"""
        hand = sorted(hand, key=rank_sort, reverse=True)
        self.analysis = Analysis(hand)
        # print hand
        # for i in range(44):
        #     print self.suit_rank_array[i]
        self.get_hand_type_value()
        self.get_hand_score(hand)
        # self.suit_rank_array = self.analysis.suit_rank_array

    def get_hand_type_value(self):
        """ given hand, it returns hand_type_value and hand_type"""
        if self.analysis.tenks > 0:
            self.hand_type_value = 20
        elif len(self.analysis.ten_card_straightflush) >= 1:
            self.hand_type_value = 19
        elif self.analysis.nineks > 0:
            self.hand_type_value = 18
        elif len(self.analysis.nine_card_straightflush) >= 1:
            self.hand_type_value = 17
        elif self.analysis.eightks > 0:
            self.hand_type_value = 16
        elif len(self.analysis.eight_card_straightflush) >= 1:
            self.hand_type_value = 15
        elif self.analysis.sevenks > 0:
            self.hand_type_value = 14
        elif len(self.analysis.seven_card_straightflush) >= 1:
            self.hand_type_value = 13
        elif self.analysis.sixks > 0:
            self.hand_type_value = 12
        elif len(self.analysis.six_card_straightflush) >= 1:
            self.hand_type_value = 11
        elif self.analysis.fiveks > 0:
            self.hand_type_value = 10
        elif len(self.analysis.five_card_straightflush) >= 1:
            self.hand_type_value = 9
        elif self.analysis.fourks > 0:
            self.hand_type_value = 8
        elif self.analysis.trips > 0 and self.analysis.pairs >= 1:
            self.hand_type_value = 7
        elif self.analysis.flushes > 0:
            self.hand_type_value = 6
        elif self.analysis.straights > 0:
            self.hand_type_value = 5
        elif self.analysis.trips > 0 and self.analysis.pairs == 0:
            self.hand_type_value = 4
        elif self.analysis.pairs > 1:
            self.hand_type_value = 3
        elif self.analysis.pairs == 1:
            self.hand_type_value = 2
        elif self.analysis.singles == 1:
            self.hand_type_value = 1
        else:
            self.hand_type_value = 1
        return self.hand_type_value
        # return self.hand_type_value

    def get_hand_type(self):
        # self.hand_type = HandType(self.hand_type_value)
        # return self.hand_type
        return(HandType(self.hand_type_value))

    def get_hand_score(self, hand):
        """ Given hand, return self.points - hand_score
            plus two digits for each of 5 cards for 11 or 12 digits,
            Also returns self.short_score for compatibility 5 or 6 digits
            """
        suits = "WCDHS"
        ranks = "0123456789TJQKA"
        # value of five cards - cards sorted by Rank then Suit from High to Low
        # self.hand = sorted(hand, key=rank_sort, reverse=True)   # not needed
        self.score = 0
        self.hand = hand
        # i is the card index, example - self.points for 81413000000 = 4 Aces with king kicker
        for i in range(len(hand)):
            self.score += ranks.index(self.hand[i][1]) * 100 ** (len(hand) - 1 - i)
        # short_score is value with last 3 card values truncated for SF, Flush and Straight and High Card
        # short_score for 81413000000 is 81413 (last 6 digits truncated)
        self.short_score = self.score // 1000000
        self.score = str(self.hand_type_value) + str(self.score)
        # print (str(self.hand_type_value))

        # short_score needs to be changed for 5K, 4K, Full House, 4K, Trip, Two Pair and Pair
        if self.hand_type_value == 6:
            self.short_score = 60000 + ranks.index(self.hand[0][1]) * 100 + ranks.index(self.hand[1][1])
        elif self.hand_type_value == 7:
            self.short_score = 70000 + ranks.index(self.analysis.trips_ranks[0]) * 100 + ranks.index(self.analysis.pairs_ranks[0])
        elif self.hand_type_value == 5:
            self.short_score = 50000 + ranks.index(self.hand[0][1]) * 100 + ranks.index(self.hand[1][1])
        elif self.hand_type_value == 4:
            if self.analysis.singles > 0:
                self.short_score = 40000 + ranks.index(self.analysis.trips_ranks[0]) * 100 + (ranks.index(self.analysis.singles_ranks[0])+50)
            else:
                # for trips, short value = hand_type_value concat trip_value concat suit1_suit2
                # need to make trip with kicker 50 higher to make it larger than suit1_suit2
                self.short_score = 40000 + ranks.index(self.analysis.trips_ranks[0]) * 100 + \
                                   (suits.index(self.hand[0][0])) * 10 + (suits.index(self.hand[1][0]))
        elif self.hand_type_value == 3:
            self.short_score = 30000 + ranks.index(self.analysis.pairs_ranks[0]) * 100 + ranks.index(self.analysis.pairs_ranks[1])
        elif self.hand_type_value == 2:
            if self.analysis.singles > 0:
                self.short_score = 20000 + ranks.index(self.analysis.pairs_ranks[0]) * 100 + ranks.index(self.analysis.singles_ranks[0])
            else:
                self.short_score = 20000 + ranks.index(self.analysis.pairs_ranks[0]) * 100
        elif self.hand_type_value == 1:
            if len(self.analysis.singles_ranks) >= 2:
                self.short_score = 10000 + ranks.index(self.hand[0][1]) * 100 + ranks.index(self.hand[1][1])
            else:
                self.short_score = 10000 + ranks.index(self.hand[0][1]) * 100 + suits.index(self.hand[0][0])
        elif len(self.hand) == 0:
            self.short_score = 10000
        elif self.hand_type_value == 8:   # four of kind
            if self.analysis.singles > 0:  # kicker
                self.short_score = 80000 + ranks.index(self.analysis.fourks_ranks[0]) * 100 + \
                                   ranks.index(self.analysis.singles_ranks[0])
            else:
                self.short_score = 80000 + ranks.index(self.analysis.fourks_ranks[0]) * 100 # no kicker
        elif self.hand_type_value in [9,11,13,15,17,19]:
            self.short_score = self.hand_type_value * 10000 + ranks.index(self.hand[0][1]) * 100 + ranks.index(self.hand[1][1])
        elif self.hand_type_value in [10,12,14,16,18,20]:
            self.short_score = self.hand_type_value * 10000 + ranks.index(self.hand[0][1]) * 100
        return

    def get_points_from_hand(self, card_list, hand):
        # try:
        new_hand = PokerHand(card_list)
        self.score = new_hand.short_score
        self.points = self.get_points_from_score(self.score, hand)
        self.points  = round(self.points, 2)
        # except:
        #     self.points = 0
        #     self.points = 0
        return [self.score, self.points]

    def get_winpoints_from_hand(self, handx, hand):
        new_hand = PokerHand(handx)
        self.score = new_hand.short_score
        self.points = self.get_winpoints_from_score(self.score, hand)
        self.points  = round(self.points, 2)
        return (self.score, self.points)

    def get_points_from_score(self, score, hand):
        """ given 1-5 cards, returns initial points and prob depending on hand number(1-6)"""
        #  print "points, hand", points, hand
        prob = self.get_hand_prob(score, hand)
        # points matrix uses same points when there are too many cards for that hand
        # each row is a hand starting from row 1 to row 6
        # each element is points won depending on score_int which is 1-12 as follows:
        # high card, 1 pair, 2 pair, trip, str, flush, fh, 4k, sf, 5k, 6sf, 6k, 7sf, 7k, 8sf, 8k, 9sf, 9k, 10sf, 10k
        points_matrix = ([0],
                         [0, 1],
                         [0, 1, 1, 1, 9, 0, 0, 0, 20, 25, 30, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40],
                         [0, 1, 1, 1, 6, 0, 0, 0, 16, 20, 24, 32, 40, 40, 40, 40, 40, 40, 40, 40, 40],
                         [0, 1, 1, 1, 3, 0, 0, 0, 12, 15, 18, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30],
                         [0, 1, 1, 1, 1, 1, 1, 2,  8, 10, 12, 16, 20, 22, 28, 28, 28, 28, 28, 28, 28],
                         [0, 1, 1, 1, 1, 1, 1, 1,  4,  5,  6,  8, 10, 11, 14, 14, 18, 17, 22, 20, 26])

        # points_array is probability of winning by each hand type value)
        points_array = (0, [0,0], [45,55], [23,67], [7,64,14, 15], [45,17,32,2,2,2], [39,26,10,16,3,3,1,1,1])
        cum_prob_of_losing_array = (0, [0, 100], [45, 100], [23, 100], [7, 71, 85, 100], [45, 62, 94, 96, 98, 100],
                                [39, 65, 75, 91, 94, 97, 98, 99, 100])
        negative_points_array = (0,[1,1], [1,9],   [1,6],   [1,3,12,15],  [1,2,8,10,12,20],  [1,4,5,6,8,10,11,14,14])
        score_int = int(score/10000)
        hand_number = int(hand)

        # win_points dependd on hand_number,score_int - ie. 4th hand, 4K (8th value) is 12 points
        # 5th hand 4K is 8 points
        win_points = points_matrix[hand_number][score_int]

        if win_points > 14:
            prob = 99.9

        # if win_points > 11:
        #     win_points = win_points * 3
        positive_points = win_points * prob
        positive_points = round(positive_points, 2)
        loss_points = win_points

        # find index for negative_points_array
        # new_index = negative_points_array[hand_number].index(loss_points)
        index = 0
        for i,n in enumerate(negative_points_array[hand_number]):
            if loss_points == n:
                index = i
                break
        # if index != new_index:
        #     print ("error in new_index", index, new_index)

        # find negative_points
        if hand_number == 1:
            negative_points = 100 - prob
        else:
            negative_points = 0
            prob_index = 0
            for i in range(index, len(negative_points_array[hand_number])):
                if i == index:
                    prob_index += cum_prob_of_losing_array[hand_number][i] - prob
                    negative_points += prob_index * loss_points
                    # print i, prob_index, loss_points, negative_points
                else:
                    negative_points += negative_points_array[hand_number][i] * points_array[hand_number][i]
                    # print i, points_array[hand_number][i], negative_points_array[hand_number][i], negative_points
        negative_points = max(0,round(negative_points,2))
        net_points = round(positive_points - negative_points,2)
        # if win_points > 11:
        #     net_points = 3 * net_points
        points = net_points

        self.score = score
        self.points = points
        # print "points, hand, prob, points, pos, neg, ev", points, hand, prob, win_points, positive_points, negative_points, expected_value

        # print "-- Score: {0:>9}, Hand: {1:>7}, Prob: {2:>7}, Points: {3:>7}, Positive: {4:>7}, Negative: {5:>7}, Expected Value: {6:>7}"\
        #    .format(points, hand, prob, win_points, positive_points, negative_points, expected_value)
        return (points)

    def get_winpoints_from_score(self, score, hand):
        """ given points, returns win_points depending hand 1,2,3,4,5,6"""
        # points matrix uses same points when there are too many cards for that hand
        points_matrix = [[0],
                         [0, 1],
                         [0, 1, 1, 1, 9, 0, 0, 0, 20, 25, 30, 40, 40],
                         [0, 1, 1, 1, 6, 0, 0, 0, 16, 20, 24, 32, 32],
                         [0, 1, 1, 1, 3, 0, 0, 0, 12, 15, 18, 24, 30, 30],
                         [0, 1, 1, 1, 1, 1, 1, 2,  8, 10, 12, 16, 20, 20, 20],
                         [0, 1, 1, 1, 1, 1, 1, 1,  4,  5,  6,  8, 10, 11, 14, 14, 18, 17, 22, 20, 26]]

        score_int = int(score/10000)
        hand_number = int(hand)
        win_points = round(points_matrix[hand_number][score_int], 2)
        self.score = score
        self.points = win_points
        return(int(win_points))

    def get_hand_prob(self, score, hand):
        global first
        global prob_dictionary
        global ProbabilityFile
        global keycount, patterncount, score_dict, update_count
        prob_dictionary = True
        if first == True:
            if prob_dictionary:
                dir_name = os.path.dirname(os.getcwd()) + '/src'
                os.chdir(dir_name)
                file = open("prob_dictionary", "rb")
                score_dict = pickle.load(file)
            else:
                CumulativeLearning()
                ProbabilityFile = ReadProbability()
            first = False
            keycount = 0
            update_count = 0
            patterncount = 0

        self.hand = hand
        self.score = score

        # score_dict is dictionary which stores "points" and "probability"
        if prob_dictionary:
            pass
        else:
            score_dict = ProbabilityFile.score_prob

        if score >= 100000:
            key = hand + str(score)
        else: key = hand + "0" + str(score)

        if key in score_dict:  # if found in dictionary
            prob = score_dict[key]
            # keycount += 1
            # print (key, "key found", "keycount:", keycount)
        else:    # if not found, then we need to use wild card search
            for i in range(1,7,1):
                # we need to go from 8 chars to 7 chars and a ".", etc
                key_start = key[0:(7-i)]
                key_end = str(i * ".")
                pattern = key_start + key_end
                patterncount += 1
                # print (key, "key not found, searching pattern", pattern, "patterncount:", patterncount)
                prob_pattern = tuple(score_dict.find(pattern))
                if prob_pattern:
                    prob = min(prob_pattern)
                    new = {key : prob}
                    # print (new, end="")
                    score_dict.update(new)   # add to dictionary
                    update_count += 1
                    if update_count >0:
                        # print("     A new points is found", update_count, key, prob)
                        get_dir()
                        file = open("prob_dictionary", "wb")
                        pickle.dump(score_dict, file)
                        file.close()
                        # WriteProb(score_dict)
                    # print ("pattern:", pattern, "found")
                    break
                else:
                    prob = .01
        self.prob = round(prob,2)
        # print ("keycount, patterncount", keycount, patterncount)
        return prob

    def get_six_hands_points(self, list_of_hands):
        hand_score = [0,0,0,0,0,0,0]
        hand_score[6] = self.get_points_from_hand(list_of_hands[6], "6")
        hand_score[5] = self.get_points_from_hand(list_of_hands[5], "5")
        hand_score[4] = self.get_points_from_hand(list_of_hands[4], "4")
        hand_score[3] = self.get_points_from_hand(list_of_hands[3], "3")
        hand_score[2] = self.get_points_from_hand(list_of_hands[2], "2")
        hand_score[1] = self.get_points_from_hand(list_of_hands[1], "1")

        for i in range (1,7):
            # print (list_of_hands[i], hand_score[i]),
            hand_score[0] = hand_score[0] + hand_score[i][1]
        hand_score[0] = round(hand_score[0],2)
        # print ("get_six_hands_points", hand_score)
        # print
        return (hand_score)

    def get_description_from_score(self,score, hand_num):

        hand_string = ['', '', 'Pair', 'TwoP', 'Trip', 'Straight',
                       'Flush', 'FullH', 'Four', 'FiveSF', 'Five', 'SixSF',
                       'Six', 'SevenSF', 'Seven', 'EightSF', 'Eight', 'NineSF',
                       'Nine', 'TenSF', 'Ten']
        handtype = int(score / 10000)
        card_rank = int((score - handtype * 10000) / 100)
        card_rank_string = ranks[card_rank]
        card_suit = score - card_rank * 100 - handtype * 10000
        card_suit_string = ""
        if handtype == 1 and hand_num == '1':
            if int(card_suit) > 4 or int(card_suit) <1:
                print ("error card suit out of range", score, hand_num, int(card_suit))
            else:
                card_suit_string = suits[int(card_suit)]
        elif handtype == 1 and hand_num != 1:
            card_suit_string = " "
        elif handtype == 4:
            card_suit_string = suits[int(card_suit/10)] + suits[int(card_suit - (card_suit / 10) * 10)]
        handtype_string = hand_string[handtype] + " " + card_suit_string + card_rank_string + ', '
        return (handtype_string)