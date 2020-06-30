import tkinter as tk
from src.Deck import *
import os

def create_card_images():
    """create all card images as a dictionary card_name:image_object"""
    # toplevel = tk.Tk()
    image_dir = "Cards_gif/"
    deck = Deck(6, 25, 3)
    card_image_dict = {}
    for card in list(deck.deck):
        # all images have filenames the match the card_list names + extension .gif
        card_only = card[0:2]
        card_image_path = image_dir + card_only + ".gif"
        # Uses the right path for Card.gif irrespective of where script is run
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent+"/src/")
        card_image_dict[card] = tk.PhotoImage(file=card_image_path)
        logging.debug("{} {}".format(card, card_image_dict[card]))
    card_image_dict["Deck3"] = tk.PhotoImage(file=image_dir+"Deck3"+".gif")
    return card_image_dict

