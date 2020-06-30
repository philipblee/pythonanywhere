import os, csv

# GAME="PP"
# NUMBER_OF_WILD_CARDS = 3
NUMBER_OF_CARDS = 25
NUM_OF_CARDS = str(NUMBER_OF_CARDS) + "CARDS"
PROBABILITY_FILE_NEW = "Probability.csv"
CUMULATIVE_LEARNING = "Cumulative_Learning.csv"
CUMULATIVE_MEDIUM_SCORES = "Cumulative_Medium_Scores.csv"

class CumulativeLearning():
    """ Reads Cumulative_Learning.csv and calculates winning_percent
        and writes results to Probability.csv"""
    def __init__(self):
        if os.path.exists(CUMULATIVE_LEARNING):
            with open(CUMULATIVE_LEARNING, "r") as g:
                reader = csv.reader(g)
                cumulative_output = list(reader)
                cumulative_learning = [[],[],[],[],[],[],[]]
            # print "learn", len(cumulative_output), "hands,"

            for item in cumulative_output:
                cumulative_learning[6].append(int(item[0]))
                cumulative_learning[5].append(int(item[2]))
                cumulative_learning[4].append(int(item[4]))
                cumulative_learning[3].append(int(item[6]))
                cumulative_learning[2].append(int(item[8]))
                cumulative_learning[1].append(int(item[10]))

            for i in range (1,7):
                cumulative_learning[i] = self.calc_win_percent(cumulative_learning[i])

            # let's write out PROBABILITY_FILE_NEW
            g = open (PROBABILITY_FILE_NEW, "w")
            g.write("0000000, 0, 0\n")

            # write out PROBABILITY_FILE
            for i in range(1,7):
                for item in cumulative_learning[i]:
                    cumulative_learning_string = str(i * 10 ** 6 + item[0]) + ", " + str(item[1]) \
                                                  + ", " + str(item[2]) + "\n"
                    with open(PROBABILITY_FILE_NEW, "a") as g:
                        g.write(cumulative_learning_string)

    def calc_win_percent(self, list_of_hands):
        """ Given a list of hands, calculate_win_percent will return
            a list of tuples corresponding to list_of_hands with
            winning percent and count
        """
        list_of_hands = sorted(list_of_hands)
        # print "calculate", len(list_of_hands)
        hand_winning_percent = [(0,0,0)]
        inum = 1
        # for each hand, count
        for i in range(len(list_of_hands)-1):
            if list_of_hands[i] == list_of_hands[i+1]:
                inum += 1
            else:
                winning_percent = round((float(i * 100)/len(list_of_hands)),4)
                hand_win_tuple = (list_of_hands[i], winning_percent, inum)
                hand_winning_percent.append(hand_win_tuple)
                inum += 1
        hand_win_tuple = (list_of_hands[i], 100, inum)
        hand_winning_percent.append(hand_win_tuple)
        hand_winning_percent = sorted(hand_winning_percent, reverse = True)
        return hand_winning_percent