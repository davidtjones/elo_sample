#!/home/david/.virtualenvs/elo/bin/python
# All links to all tournaments, events

import requests
from tabulate import tabulate
import numpy as np
import bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.io import export_png
from bokeh.palettes import Spectral4
from bokeh.sampledata.stocks import AAPL, IBM, MSFT, GOOG
from pprint import pprint
import json
import pickle
import os

from config import api_key

rerun = False
path = 'league.json'

from classes import Player, Set, Tournament, League
from scoring import elo_sort

print("Forward Smash Rankings 2018")

# Build League
if(rerun or not os.path.exists(path)):
    events = {
          "SB1" : [None, False],
          "SB2" : ['https://api.challonge.com/v1/tournaments/Smashmas2016/', True, 'T'],
          "SB3" : [None, False],
          "SB4" : ['https://api.challonge.com/v1/tournaments/cnf6kpmn/', True, 'T'],
          "C1"  : ['https://api.challonge.com/v1/tournaments/smashclashone/', True, 'T'],
          "C2"  : ['https://api.challonge.com/v1/tournaments/smashclashtwo/', True, 'T'],
          "Cinco" : ['https://api.challonge.com/v1/tournaments/5daymayo/', True, 'T'],
          "C3" : ['https://api.challonge.com/v1/tournaments/smashclashthree/', True, 'T'],
          "M1" : ['https://api.challonge.com/v1/tournaments/n4d95xuj/', True, 'M'],
          "M2" : ['https://api.challonge.com/v1/tournaments/belcan_smash_monthly_2/', True, 'M']
    }

    league = League("Forward Smash", events)
    league.save(path)

else:
    # Read from JSON
    print("Reading from File")
    league = League("Forward Smash", None)
    league.load(path)
    
print("%s has %s players and %s tournaments with %s sets."%(league.get_info()))


for name, player in league.get_players().items():
    player.reset_rank()

league.processRanks(decay_val=20, method='elo', decay=False, delay=1, decay_monthlies=False)
league.save('noDecayResults.json')   

print(tabulate(elo_sort(league.get_players())))


for name, player in league.get_players().items():
    player.reset_rank()
league.save(path)

league.processRanks(decay_val=20, method='elo', decay=True, delay=1, decay_monthlies=False)
league.save('decayResults.json')

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
