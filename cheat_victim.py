import datetime
import random
import numpy
import math

def count_cheat_victim(killers, victims, dates):
    '''
    Takes in three arguments: killers, victims, and date. 
    Reads the files, and counts number of instances where cheater kills another cheater by reading cheater ids & start/end dates.
    Returns the count.
    '''
    cheater_ids = [] 
    dates_of_start = [] 
    dates_of_banning = [] 
    
    with open('./cheaters.txt','r') as f:
        for line in f:
            cheater_id, date_of_start, date_of_banning = line.split()
            cheater_ids.append(cheater_id)
            dates_of_start.append(datetime.datetime.strptime(date_of_start, "%Y-%m-%d"))
            dates_of_banning.append(datetime.datetime.strptime(date_of_banning, "%Y-%m-%d"))
    
    count = 0
    for i in range(len(killers)):
        if killers[i] in cheater_ids and victims[i] in cheater_ids: 
            date = dates[i]
            if killers[i] in cheater_ids:
                k_index = cheater_ids.index(killers[i])
                if dates_of_start[k_index] <= date and date < dates_of_banning[k_index]: 
                    if victims[i] in cheater_ids:
                        v_index = cheater_ids.index(victims[i])
                        if date < dates_of_start[v_index]:
                            count += 1
    return count


def victim_cheat_checker():
    '''
    the main function.
    calls the other function, reads the files, and returns the actual & expected results.
    the expected results are kept with 3 decimal spaces for clear visual purpose.
    '''
    cheater_ids = [] 
    dates_of_start = [] 
    dates_of_banning = [] 
    killer_ids = []
    victim_ids = [] 
    dates_of_kills = []
    
    with open('./cheaters.txt','r') as f:
        for line in f: 
            cheater_id, date_of_start, date_of_banning = line.split()
            cheater_ids.append(cheater_id)
            dates_of_start.append(datetime.datetime.strptime(date_of_start, "%Y-%m-%d"))
            dates_of_banning.append(datetime.datetime.strptime(date_of_banning, "%Y-%m-%d"))
            
    with open('./kills.txt','r') as f:
        for line in f: 
            match_id, killer_id, victim_id, date, time = line.split()
            killer_ids.append(killer_id)
            victim_ids.append(victim_id)
            dates_of_kills.append(datetime.datetime.strptime(date, "%Y-%m-%d"))
    
    result = count_cheat_victim(killer_ids,victim_ids, dates_of_kills)
    
    print("The number of victims starting cheating is: " + str(result))
    print("Now calculating the expected result...")

    total = []
    for i in range(20):
        random.shuffle(killer_ids)
        random.shuffle(victim_ids)    
        total.append(count_cheat_victim(killer_ids, victim_ids, dates_of_kills))
    lower_bound = numpy.mean(total) - 1.96 * numpy.std(total) / math.sqrt(20)
    upper_bound = numpy.mean(total) + 1.96 * numpy.std(total) / math.sqrt(20)

    print("The expected number of victims starting cheating is: " + '')
    print('({:.3f}, {:.3f})'.format(lower_bound, upper_bound))
    return "Calculation Finished"