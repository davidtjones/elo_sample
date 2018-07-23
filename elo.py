# All links to all tournaments, events
import requests
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import json
import pickle
import os

from classes import Player, Set, Tournament, League
print("testing scoring 2")
events = {
      "SB1" : [None, False],
      "SB2" : ['https://api.challonge.com/v1/tournaments/Smashmas2016/', True],
      "SB3" : [None, False],
      "SB4" : ['https://api.challonge.com/v1/tournaments/cnf6kpmn/', True],
      "C1"  : ['https://api.challonge.com/v1/tournaments/smashclashone/', True],
      "C2"  : ['https://api.challonge.com/v1/tournaments/smashclashtwo/', True],
      "Cinco" : ['https://api.challonge.com/v1/tournaments/5daymayo/', True],
      "C3" : ['https://api.challonge.com/v1/tournaments/smashclashthree/', True],
      "M1" : ['https://api.challonge.com/v1/tournaments/n4d95xuj/', True]
}

league = League("Forward Smash")
path = 'league.json'
# Build League
if(not os.path.isfile(path)):
    # Generate from API
    print("Generating via API")
    api_key = 'BVfAkPtSZ5d3DzWrQfAnrwlq8cHGRSN67eTDgRra' #pls don't steal

    for name, data in events.items():
        if(events[name][0] != None):
            t = Tournament(name, data[0], data[1])
            res = league.add_tournament(t)
            if (res ==  True):
                t.fetch_sets(api_key)
                sets = t.get_sets()
                print("total number of sets in %s: %s"%(name, len(sets)))



    league.preprocess_sets()


    f = open('league.json', 'w', encoding='utf8')
    f.write(league.toJSON())
    f.close()

else:
    # Read from JSON
    print("Reading from File")
    league.load(path)
    #pprint(league.toJSON())
    t = league.get_tournaments()
    #print(league.toJSON())
    print("%s has %s players and %s tournaments"%(league.get_info()))

# League object is now built, rankings can be performed easily!

for name, player in league.get_players().items():
    player.reset_rank()

def elo_score_set(winner, loser):
    if((winner.get_rank_current()) == None): winner.set_rank_current(1200)
    if((loser.get_rank_current()) == None): loser.set_rank_current(1200)
    
    P1 = (1.0 / (1.0 + (10**((loser.get_rank_current() - winner.get_rank_current())/400))))
    P2 = (1.0 / (1.0 + (10**((winner.get_rank_current() - loser.get_rank_current())/400))))
    
    #choose lowest K
    low_K = winner.get_K() if winner.get_K() <= loser.get_K() else loser.get_K()
    
    w_new_rank = winner.get_rank_current() + low_K * (1 - P1)
    l_new_rank = loser.get_rank_current() + low_K * (0 - P2)

    winner.set_rank_current(w_new_rank)
    loser.set_rank_current(l_new_rank)
    return

# f = open('league.json', 'w', encoding='utf8')
# f.write(league.toJSON())
# f.close()

tournaments = league.get_tournaments()
players = league.get_players()
for name, tournament in tournaments.items():
    # apply ranking algorithm for each match in each set:
    t_sets = tournament.get_sets()
    print("\nTournament: %s\n"%(name))
    for c_set in t_sets:
        winner = league.get_player(c_set["winner"])
        loser = league.get_player(c_set["loser"])
        print("Scoring %s (%s) vs %s (%s)"%(winner.get_name(), winner.get_rank_current(), loser.get_name(), loser.get_rank_current()))
        elo_score_set(winner, loser)
        print("Scored  %s (%s) vs %s (%s)"%(winner.get_name(), winner.get_rank_current(), loser.get_name(), loser.get_rank_current()))
        winner.add_set(name, c_set)
        loser.add_set(name, c_set)
        
    
    for name, player in players.items():
        player.commit_rank()
    
    
        

f = open('league.json', 'w', encoding='utf8')
f.write(league.toJSON())
f.close()


def elo_sort(players):
    plist = []
    for name, player in players.items():
        plist.append((name, player.get_rank_current()))

    #filter none types
    #list(filter((None).__ne__, rankings))
    plist_f = list(filter(lambda x: x[1] != None, plist))
    #print(rankings)

    #sort remainder of list
    plist_s = sorted(plist_f, key=lambda x: x[1], reverse=True)

    return plist_s


print(tabulate(elo_sort(league.get_players())))

ranks_dt = []
for name, player in league.get_players().items():
    temp = [name]
    temp.extend(player.get_rank_history())
    ranks_dt.append(temp)

print(tabulate(ranks_dt))