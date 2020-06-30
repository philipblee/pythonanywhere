suit = "CDHSW"
rank = "123456789TJQKAW"

def suit_rank_sort(a):
    """ sorts by suit then rank"""
    return(suit.index(a[0])*14 + rank.index(a[1]))

def rank_sort(a):
    """ sorts by rank then suit"""
    return(rank.index(a[1])*10 + suit.index(a[0]))