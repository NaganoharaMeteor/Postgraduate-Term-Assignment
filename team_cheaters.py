import random
import numpy
import math

def count_teamed_cheaters(data_dict):
    cheater_ids = [] 
    dates_of_banning = []
    with open('./cheaters.txt','r') as f:
        for line in f:
            cheater_id, date_of_start, date_of_banning = line.split()
            cheater_ids.append(cheater_id)
            dates_of_banning.append(date_of_banning)
    teamed_cheaters = {}
                        
    for match_id, match_data in data_dict.items():
        players, teams = match_data
        for i in range(len(players)):
            team_id = match_id + '.' + teams[i]
            if team_id not in teamed_cheaters:
                if players[i] in cheater_ids:
                    teamed_cheaters[team_id] = 1
                else:
                    teamed_cheaters[team_id] = 0
            elif players[i] in cheater_ids:
                teamed_cheaters[team_id] += 1
    
    teams_with_0_cheater = sum(val == 0 for val in teamed_cheaters.values())
    teams_with_1_cheater = sum(val == 1 for val in teamed_cheaters.values())
    teams_with_2_cheater = sum(val == 2 for val in teamed_cheaters.values())
    teams_with_3_cheater = sum(val == 3 for val in teamed_cheaters.values())
    teams_with_4_cheater = sum(val == 4 for val in teamed_cheaters.values())
    
    return teams_with_0_cheater, teams_with_1_cheater, teams_with_2_cheater, teams_with_3_cheater, teams_with_4_cheater

def calc_conf_interval(data):
    '''
    calculates the confidence interval.
    '''
    data = numpy.array(data)
    lower_bound = numpy.mean(data) - 1.96 * numpy.std(data) / math.sqrt(20)
    upper_bound = numpy.mean(data) + 1.96 * numpy.std(data) / math.sqrt(20)
    print('({:.3f}, {:.3f})'.format(lower_bound, upper_bound))

def if_cheater_teamed():
    '''
    the main function.
    calls the other function, reads the files, and returns the actual & expected results.
    the expected results are kept with 3 decimal spaces for clear visual purpose.
    '''
    teamed_players = {}
    with open('./team_ids.txt','r') as f:
        for line in f:
            match_id, player, team = line.split()
            if match_id not in teamed_players:
                teamed_players[match_id] = [[],[]]
            else:
                teamed_players[match_id][0].append(player) 
                teamed_players[match_id][1].append(team) 
                
    counts = count_teamed_cheaters(teamed_players)
    print('There are', counts[0], 'teams with 0 cheater.')
    print('There are', counts[1], 'teams with 1 cheater.')
    print('There are', counts[2], 'teams with 2 cheaters.')
    print('There are', counts[3], 'teams with 3 cheaters.')
    print('There are', counts[4], 'teams with 4 cheaters.')
    
    print('Now calculating the expected results...')
    total = [[] for i in range(5)]
    for i in range(20):
        for match in teamed_players.keys():
            random.shuffle(teamed_players[match][1])
        counts = count_teamed_cheaters(teamed_players)
        for i in range(5):
            total[i].append(counts[i])
            
    print('Expecting the number teams of 0 cheater to be:', end='')
    calc_conf_interval(total[0])
    print('Expecting the number teams of 1 cheater to be:', end='')
    calc_conf_interval(total[1])
    print('Expecting the number teams of 2 cheaters to be:', end='')
    calc_conf_interval(total[2])
    print('Expecting the number teams of 3 cheaters to be:', end='')
    calc_conf_interval(total[3])
    print('Expecting the number teams of 4 cheaters to be:', end='')
    calc_conf_interval(total[4])
