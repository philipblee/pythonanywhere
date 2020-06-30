import re
from src.PokerHand import *
import csv

class ScoreProb(dict):

    """ ScoreProb is a class that is based on Python's dict class """
    def find(self, dict):
        """ find looks for pattern match in the dictionary
            example:  pattern= "604...." looks for keys that begin with 604 in dictionary
            """
        return (self[pattern] for pattern in self if re.match(dict, pattern))

class ReadProbability():
    """ class reads PROBABILITY_FILE_NEW2 and stores into score_prob
        which is a dictionary with a find method for pattern matching
        when the exect match cannot be found in dictionary"""
    def __init__(self):
        # my_hand = Hand()
        import os
        rel_path = "Probability.csv"
        cwd = os.getcwd()


        with open(rel_path, "r") as e:
            reader = csv.reader(e)
            x = list(reader)
        self.score_prob = ScoreProb()
        self.score_points = ScoreProb()
        for a in x:
            self.score_prob [str(a[0])] = float(a[1])
            hand = int(a[0][0])
            score = int(a[0][1:])
