from src.straight_count import straight_count
from src.sort_cards import rank_sort, suit_rank_sort
from itertools import *

ranks = "W123456789TJQKA"
suits = "WSHDC"
straight_ranks = "WA23456789TJQKA"

class Analysis(list):
    """ This class takes a list of cards and provides complete analysis in
    the form of suit_rank_array.  It also provides a series of attributes
    with descriptive names at the end of the program
    returns suit_rank_array[i] where i is row
     0 - W                11 - singles_list    21 - S_list        31 - ranks of 11     41 - ranks of spades
     1 - S                12 - pairs_list      22 - H_list        32 - ranks of 12     42 - ranks of hearts
     2 - H                13 - trips_list      23 - D_list        33 - ranks of 13     43 - ranks of diamonds
     3 - D                14 - fourks_list     24 - C_list        34 - ranks of 14     44 - ranks of clubs
     4 - C                15 - fiveks_list     no 25 - 5 card SF  35 - ranks of 15     45 - 5 card SF
     5 - Frequency        16 - sixks_list      no 26 - 6 card SF  36 - ranks of 16     46 - 6 card SF
     6 - Straights        17 - sevenks_list    no 27 - 7 card SF  37 - ranks of 17     47 - 7 card SF
     no 7 - SF S          18 - eightks_list    no 28 - 8 card SF  38 - ranks of 18     48 - 8 card SF
     no 8 - SF H          19 - nineks_list     no 29 - 9 card SF  39 - ranks of 19     49 - 9 card SF
     no 9 - SF D          20 - tenks_list      no 30 - 10 card SF 40 - ranks of 20     50 - 10 card SF
     no 10 - SF C

     cards are stored in rows 11 to 30; only ranks are stored in rows 31 to 44;
     list of SF's are stored in 45-50
     column 15 is always sum of row - for flushes [5][15], sf totals [7][14]
     """

    def __init__(self, card_list):

        self.desc = ['W', 'S', 'H', 'D', 'C', 'Frequency', 'Straights' , 'n/a', 'n/a', 'n/a', 'n/a',
                    'singles_list', 'pairs_list', 'trips_list', 'fourks_list', 'fiveks_list', 'sixks_list',
                     'sevenks_list', 'eightks_list', 'nineks_list', 'tenks_list',
                     'S_list', 'H_list', 'D_list', 'C_list',
                     '5 card SF', '6 card SF', '7 card SF', '8 card SF', '9 card SF', '10 card SF',
                     'ranks of 11', 'ranks of 12', 'ranks of 13', 'ranks of 14', 'ranks of 15',
                     'ranks of 16', 'ranks of 17', 'ranks of 18', 'ranks of 19', 'ranks of 20',
                     'ranks of spades', 'ranks of hearts', 'ranks of diamonds', 'ranks of clubs',
                     '5 card SF', '6 card SF', '7 card SF', '8 card SF', '9 card SF', '10 card SF']

        suit_rank_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for i in range(7)]
        suit_rank_array += [[] for i in range(44)]

        self.suit_rank_array = suit_rank_array

        # self.card_list must be sorted in rank_sort reverse order, otherwise it analyzes incorrectly
        self.card_list = sorted(card_list, key=rank_sort, reverse=True) # this is needed because wild_cards not sorted
        self.decode_cards()  # puts cards in rows 0-4
        self.store_flushes()   # puts number of flushes in column 15 for rows 0-4
        self.store_frequencies()   # puts frequencies in row 5
        self.max_frequency = max(self.suit_rank_array[5][1:15])
        suit_rank_array[6] = straight_count(suit_rank_array[5], 5)    # puts straights in row 6
        self.split_into_lists()    # splits into lists in rows 11-20
        self.straight_flushes()     # puts straight flushes in rows 45-50
        self.store_ranks()     # in rows 31-40
        self.store_names()
        # for i in range(0, 51):
        #     print(i, suit_rank_array[i])
        return

    def decode_cards(self):   # rows 0-4, 21-24, 41-44
        """ takes card_list and stores them in array for counting"""
        for card in reversed(self.card_list):
            suit_int = suits.index(card[0])  # 1:5
            rank_int = ranks.index(card[1])  # 1:15
            self.suit_rank_array[suit_int][rank_int] += 1  # increment[i][j] by 1
            if suit_int != 0: # if it's not wild card
                self.suit_rank_array[20 + suit_int].append(card)  # store cards of each suit in rows 21:24
                self.suit_rank_array[40 + suit_int].append(card[1])  # store ranks of each suit in rows 41:44
        return

    def store_flushes(self):  # cell 5,15
        for i in range(5):
            self.suit_rank_array[i][15] = sum(self.suit_rank_array[i][0:15])  # put suit counts in 15
            self.suit_rank_array[i][1] = self.suit_rank_array[i][14]  # set up Ace as 1 for straights
            if self.suit_rank_array[i][15] >= 5:
                self.suit_rank_array[5][15] += 1   # count suits that have >= 5 cards and put in [5][15]
        return

    def store_frequencies(self): # row 5
        for j in range(1, 15):  # puts frequency of card rank in row 5
            self.suit_rank_array[5][j] = self.suit_rank_array[0][j] + self.suit_rank_array[1][j]+ \
                                         self.suit_rank_array[2][j]+ self.suit_rank_array[3][j]+ self.suit_rank_array[4][j]

        self.highest_rank_gt_pair = 1
        for j in range(14, 0, -1):
            # print ("finding j2", j, self.suit_rank_array[5][j])
            if self.suit_rank_array[5][j] > 0:
                self.highest_rank_gt_pair = j
                break
        return

    def store_names(self):
        # counts for straight flushes, flushes and straights
        self.five_card_straightflushes = len(self.suit_rank_array[45])
        self.flushes = self.suit_rank_array[5][15]
        self.straights = self.suit_rank_array[6][15]

        # cards
        self.singles_list = self.suit_rank_array[11]
        self.pairs_list = self.suit_rank_array[12]
        self.trips_list = self.suit_rank_array[13]
        self.fourks_list = self.suit_rank_array[14]
        self.fiveks_list = self.suit_rank_array[15]
        self.sixks_list = self.suit_rank_array[16]
        self.sevenks_list = self.suit_rank_array[17]
        self.eightks_list = self.suit_rank_array[18]
        self.nineks_list = self.suit_rank_array[19]
        self.tenks_list = self.suit_rank_array[20]

        # ranks
        self.singles_ranks = self.suit_rank_array[31]
        self.pairs_ranks = self.suit_rank_array[32]
        self.trips_ranks = self.suit_rank_array[33]
        self.fourks_ranks = self.suit_rank_array[34]
        self.fiveks_ranks = self.suit_rank_array[35]
        self.sixks_ranks = self.suit_rank_array[36]
        self.sevenks_ranks = self.suit_rank_array[37]
        self.eightks_ranks = self.suit_rank_array[38]
        self.nineks_ranks = self.suit_rank_array[39]
        self.tenks_ranks = self.suit_rank_array[40]

        # count
        self.singles = len(self.singles_list)
        self.pairs = len(self.pairs_list)
        self.trips = len(self.trips_list)
        self.fourks = len(self.fourks_list)
        self.fiveks = len(self.fiveks_list)
        self.sixks = len(self.sixks_list)
        self.sevenks = len(self.sevenks_list)
        self.eightks = len(self.eightks_list)
        self.nineks = len(self.nineks_list)
        self.tenks = len(self.tenks_list)
        self.wilds = self.suit_rank_array[5][0]

        # initial cards of x-card straight flushes
        self.five_card_straightflush = self.suit_rank_array[45]
        self.six_card_straightflush = self.suit_rank_array[46]
        self.seven_card_straightflush = self.suit_rank_array[47]
        self.eight_card_straightflush = self.suit_rank_array[48]
        self.nine_card_straightflush = self.suit_rank_array[49]
        self.ten_card_straightflush = self.suit_rank_array[50]

        # lists of x of a kind and greater
        self.ninekx_list = self.nineks_list + self.tenks_list
        self.eightkx_list = self.eightks_list + self.ninekx_list
        self.sevenkx_list = self.sevenks_list + self.eightkx_list
        self.sixkx_list = self.sixks_list + self.sevenkx_list
        self.fivekx_list = self.fiveks_list + self.sixkx_list
        self.fourkx_list = self.fourks_list + self.fivekx_list
        self.tripx_list = self.fourkx_list + self.trips_list

        # print("new run of Analysis", self.card_list)
        # for i in range(51):
        #     print (self.suit_rank_array[i])
        return

    def straight_flushes(self):
        # n-card straight flush
        n_card_straight_flushes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # reduce range based on max number of flush cards/suit
        max_flush_cards = max(self.suit_rank_array[1][15], self.suit_rank_array[2][15], self.suit_rank_array[3][15], self.suit_rank_array[4][15])
        if max_flush_cards > 10:
            max_flush_cards = 10
        for n in range(5, max_flush_cards + 1):   # if max_flush_cards = 10, n is range(5,10)
            straight_ct = 5 * [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
            for i in range(1,5):
                if self.suit_rank_array[i][15] >= n:
                    straight_ct[i] = straight_count(self.suit_rank_array[i], n)
            n_card_straight_flushes[n] = straight_ct[1][15] + straight_ct[2][15] + straight_ct[3][15] + straight_ct[4][15]

            if n_card_straight_flushes[n] > 0:
                for i in range(1, 5):
                    for j in range(15 - n, 0, -1):
                        if straight_ct[i][j] > 0:
                            # find n consecutive cards in suit[i]
                            straight_card = [[], [], [], [], [], [], [], [], [], []]
                            for k in range(n):
                                for card in self.card_list:
                                    if straight_ranks[j + k] in card and suits[i] in card:
                                        straight_card[k].append(card)
                            # store entire straight_flush in 45-50 depending on n
                            if n == 5:
                                for straight_hand in list(product(straight_card[0], straight_card[1],
                                                straight_card[2], straight_card[3], straight_card[4])):
                                    self.suit_rank_array[40 + n].append(straight_hand)
                                    self.suit_rank_array[20 + n].append(straight_hand)
                            elif n == 6:
                                for straight_hand in list(product(straight_card[0], straight_card[1], straight_card[2],
                                                                  straight_card[3], straight_card[4], straight_card[5])):
                                    self.suit_rank_array[40 + n].append(straight_hand)
                                    self.suit_rank_array[20 + n].append(straight_hand)
                            elif n == 7:
                                for straight_hand in list(
                                        product(straight_card[0], straight_card[1], straight_card[2], straight_card[3],
                                                straight_card[4], straight_card[5], straight_card[6])):
                                    self.suit_rank_array[40 + n].append(straight_hand)
                                    self.suit_rank_array[20 + n].append(straight_hand)
                            elif n == 8:
                                for straight_hand in list(
                                        product(straight_card[0], straight_card[1], straight_card[2], straight_card[3],
                                                straight_card[4], straight_card[5], straight_card[6], straight_card[7])):
                                    self.suit_rank_array[40 + n].append(straight_hand)
                                    self.suit_rank_array[20 + n].append(straight_hand)
                            elif n == 9:
                                for straight_hand in list(
                                        product(straight_card[0], straight_card[1], straight_card[2], straight_card[3],
                                                straight_card[4], straight_card[5], straight_card[6], straight_card[7],
                                                straight_card[8])):
                                    self.suit_rank_array[40 + n].append(straight_hand)
                                    self.suit_rank_array[20 + n].append(straight_hand)
                            elif n == 10:
                                for straight_hand in list(
                                    product(straight_card[0], straight_card[1], straight_card[2], straight_card[3],
                                            straight_card[4], straight_card[5], straight_card[6], straight_card[7],
                                            straight_card[8], straight_card[9])):
                                    self.suit_rank_array[40 + n].append(straight_hand)
                                    self.suit_rank_array[20 + n].append(straight_hand)
        return

    def store_ranks(self):
        # Store in rows 31-40, ranks of singles, pairs, trips, etc etc.
        for j in range(self.highest_rank_gt_pair, 1, -1):
            if self.suit_rank_array[5][j] > 0:
                if self.suit_rank_array[5][j] == 1:
                    self.suit_rank_array[31].append(ranks[j])
                elif self.suit_rank_array[5][j] == 2:
                    self.suit_rank_array[32].append(ranks[j])
                elif self.suit_rank_array[5][j] == 3:
                    self.suit_rank_array[33].append(ranks[j])
                elif self.suit_rank_array[5][j] == 4:
                    self.suit_rank_array[34].append(ranks[j])
                elif self.suit_rank_array[5][j] == 5:
                    self.suit_rank_array[35].append(ranks[j])
                elif self.suit_rank_array[5][j] == 6:
                    self.suit_rank_array[36].append(ranks[j])
                elif self.suit_rank_array[5][j] == 7:
                    self.suit_rank_array[37].append(ranks[j])
                elif self.suit_rank_array[5][j] == 8:
                    self.suit_rank_array[38].append(ranks[j])
                elif self.suit_rank_array[5][j] == 9:
                    self.suit_rank_array[39].append(ranks[j])
                elif self.suit_rank_array[5][j] == 10:
                    self.suit_rank_array[40].append(ranks[j])
        return

    def split_into_lists(self):
        # go through each card and put in suit_rank_array 11-20 based on frequency of rank
        for card in self.card_list:
            frequency = self.suit_rank_array[5][ranks.index(card[1])]
            self.suit_rank_array[10 + frequency].append(card)
        max_frequency = max(self.suit_rank_array[5][1:15])
        # split into multiple lists for rows 11 to 20
        for size in range(2, max_frequency + 1):
            seq = self.suit_rank_array[10 + size]
            self.suit_rank_array[10 + size] = [seq[i:i + size] for i in range(0, len(seq), size)]
        return