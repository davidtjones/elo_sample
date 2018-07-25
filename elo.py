# All links to all tournaments, events
import requests
from tabulate import tabulate
import numpy as np
import bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.io import export_png
from bokeh.palettes import Spectral4
from bokeh.sampledata.stocks import AAPL, IBM, MSFT, GOOG
import numpy as np
from pprint import pprint
import json
import pickle
import os

rerun = True

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
if(not os.path.isfile(path) and rerun):
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


for name, player in league.get_players().items():
    player.reset_rank()


league.processRanks()

#league.save('league.json')       

print(tabulate(elo_sort(league.get_players())))


for name, player in league.get_players().items():
    player.reset_rank()
    

league.processRanks(decay=True)
























#
# Results
#



print(tabulate(elo_sort(league.get_players())))

# ranks_dt = []
# for name, player in league.get_players().items():
#     temp = [name]
#     temp.extend(player.get_rank_history())
#     ranks_dt.append(temp)

# ranks_dt_s = sorted(ranks_dt, key=lambda x: x[7], reverse=True)

# print(tabulate(ranks_dt_s, showindex='always', headers=['Name', 'SB2', 'SB4', 'C1', 'C2', 'Cinco', 'C3', 'M1']))
# pprint(AAPL.keys())
# ##  Visualizations
# FSMASH = {}
# t = ["SB2", "SB4", "C1", "C2", "Cinco", "C3", "M1"]
# for tournament in t:
#     FSMASH{tournament} = []
#     for rank in rank_dt:
        





# p = figure(plot_width=800, plot_height=250) #, x_axis_type="datetime")
# p.title.text = 'Click on legend entries to hide the corresponding lines'

# for data, name, color in zip((xs, ys), names, Spectral4):
#     p.line(data[0], data[1], line_width=2, color=color, alpha=.8, legend=name)

# p.legend.location = "top_left"
# p.legend.click_policy="hide"

#output_file("interactive_legend.html", title="interactive_legend.py example")

#show(p)

#######################

    
# # print(names)
# # print(ys)
# # print(xs)

# output_file("ranks_dt.html")
# p = figure(title="Ranks Over Time", x_axis_label='time', y_axis_label='rank')
# p.xaxis.ticker = [0, 1, 2, 3, 4, 5, 6, 7]
# p.xaxis.major_label_overrides = {0: 'SB2', 1: 'SB4', 2: 'C1', 3: 'C2', 4: 'Cinco', 5: 'C3', 6: 'M1'}

# p.multi_line(xs, ys, names)
# show(p)