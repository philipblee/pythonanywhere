def straight_count (rankcount, length):
    """ count straights - takes in rankcount(list of ranks), and returns straightct
        array with straights in straightct [1:10] - if 1, it's A2345, if 2 it's23456
        finally straightct [15] = total number of straights
        used mainly by analyze()"""
    straightct = 16 * [0]
    # print "straigth_ct", rankcount[1:15], sum(rankcount[0:15]), length
    if sum(rankcount) > length-1:
        count = 0
        for i in range(1, 15):
            if rankcount[i] > 0:
                count += 1
            else:
                count = 0
            # count == length of straight, then I found 1 straight found
            if count == length:
                # straight quantity counts additional straights based on multiples of each card
                straight_quantity = 1
                for j in range (i-length+1,i+1):
                    straight_quantity *= rankcount[j]
                straightct[i-length+1] = 1 * straight_quantity
                count = length - 1
        straightct[15] = sum(straightct)
    return(straightct)
