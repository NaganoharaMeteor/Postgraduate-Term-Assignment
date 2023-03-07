import datetime
import random
import numpy
import math

def three_kills_check(killer, victim, deaths, victims):
    '''check if the victim is killed more than 3 times'''
    count = 0
    if victim in victims:
        for i in range(victims.index(victim)):
            if deaths[i] == killer:
                count += 1
    return count >= 3

def count_cheat_ob(killers, victims, dates):
    '''
    Takes in three arguments: killers, victims, and date. 
    Reads the file and checks for cheaters involved in the kills during the ban period and if the victim was not a cheater before the killer's ban period starts. 
    Returns the count of the number of times a cheater killed another cheater during their ban period.
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
        for j in range(len(killers[i])):
            killer = killers[i][j]
            victim = victims[i][j]
            kill_date = datetime.datetime.strptime(dates[i][j], "%Y-%m-%d")
            
            if killer in cheater_ids and victim in cheater_ids:
                start_date = dates_of_start[cheater_ids.index(killer)]
                end_date = dates_of_banning[cheater_ids.index(killer)]
                victim_start_date = dates_of_start[cheater_ids.index(victim)]
                
                if start_date <= kill_date and kill_date < end_date:
                    if kill_date < victim_start_date:
                        if three_kills_check(killer, victim, killers[i], victims[i]):
                            count += 1
    return count

def ob_cheat_checker():
    '''
    the main function.
    calls the other function, reads the files, and returns the actual & expected results.
    the expected results are kept with 3 decimal spaces for clear visual purpose.
    '''
    cheater_ids = [] 
    dates_of_start = [] 
    dates_of_banning = [] 
    dates_of_match = []
    match_killer = [] 
    match_victim = []
    match = '1' 
    match_i = -1 
    
    with open('./cheaters.txt','r') as f:
        for line in f: 
            cheater_id, date_of_start, date_of_banning = line.split()
            cheater_ids.append(cheater_id)
            dates_of_start.append(date_of_start)
            dates_of_banning.append(date_of_banning)
            
    with open('./kills.txt','r') as f:
        for line in f: 
            match_id, killer_id, victim_id, date, time = line.split()
            if match_id != match:
                match_i += 1
                match_killer.append([])
                match_victim.append([])
                dates_of_match.append([])
            match = match_id
            match_killer[match_i].append(killer_id)
            match_victim[match_i].append(victim_id)
            dates_of_match[match_i].append(date)
    result = count_cheat_ob(match_killer, match_victim, dates_of_match)
    
    print("The number of observers starting cheating is: " + str(result))
    print("Now calculating the expected results...")

    total = []
    for i in range(20):
        for i in range(len(match_killer)):
            random.shuffle(match_killer[i])
            random.shuffle(match_victim[i])
        total.append(count_cheat_ob(match_killer, match_victim, dates_of_match))
    lower_bound = numpy.mean(total) - 1.96 * numpy.std(total) / math.sqrt(20)
    upper_bound = numpy.mean(total) + 1.96 * numpy.std(total) / math.sqrt(20)
    
    print("The expected number of observers starting cheating is: " + '')
    print('({:.3f}, {:.3f})'.format(lower_bound, upper_bound))
    return "Calculation Finished"