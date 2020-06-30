""" display_points is a function to display points of 6 hands and total
    display_points_clear is a function to clear out points from last hand
"""

import tkinter as tk

def display_points(score_array, x2, y2):
    """
    given score_array displays 6 scores and total points at x,y coordinates
    :param score_array: score0, score1, score2, score2, score3, score4, score5, score6
    :param x: x coordinate of where to display_points
    :param y: y coordinate of where to display_points
    """
    # display_points_clear(x2,y2)
    score = score_array
    fill = 0
    total_score_label = tk.Label(text="total =  " + str(score[0]) + fill*" ", fg="blue", bg="white", font=12)
    total_score_label.place(x=x2, y=y2)
    hand6_score_label = tk.Label(text="hand6 = " + str(score[6]) + fill*" ", fg="blue", bg="white", font=12)
    hand6_score_label.place(x=x2, y=y2 + 25)
    hand5_score_label = tk.Label(text="hand5 = " + str(score[5]) + fill*" ", fg="blue", bg="white", font=12)
    hand5_score_label.place(x=x2, y=y2 + 50)
    hand4_score_label = tk.Label(text="hand4 = " + str(score[4]) + fill*" ", fg="blue", bg="white", font=12)
    hand4_score_label.place(x=x2, y=y2 + 75)
    hand3_score_label = tk.Label(text="hand3 = " + str(score[3]) + fill*" ", fg="blue", bg="white", font=12)
    hand3_score_label.place(x=x2, y=y2 + 100)
    hand2_score_label = tk.Label(text="hand2 = " + str(score[2]) + fill*" ", fg="blue", bg="white", font=12)
    hand2_score_label.place(x=x2, y=y2 + 125)
    hand1_score_label = tk.Label(text="hand1 = " + str(score[1]) + fill*" ", fg="blue", bg="white", font=12)
    hand1_score_label.place(x=x2, y=y2 + 150)

def display_points_clear(x1, y1):
    fill = 120
    total_score_label = tk.Label(text = fill*" ", bg="light blue", height = 26)
    total_score_label.place(x=x1, y=y1)
