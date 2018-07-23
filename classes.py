import requests
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import json
import pickle


# Class Definitions
class JsonSerializable():
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

    def __repr__(self):
        return self.toJSON()


class Player(JsonSerializable):
    def __init__(self, name):
        self.name = name
        self.rank_current = None
        self.rank_history = [] # no score if the player hasn't played a ranked match yet
        #self.handles = []
        self.K = 20
        self.is_ranked = True
        self.sets = {}


    def __str__(self):
        return self.name
   
    def get_name(self):
        return self.name

    def set_rank_current(self, num):
        self.rank_current = num
    
    def reset_rank(self):
        self.rank_history = []
        self.rank_current = None

    def get_rank_current(self):
        return self.rank_current

    def get_rank_history(self):
        return self.rank_history
    
    def set_rank_history(self, rank_history):
        self.rank_history = rank_history

    def commit_rank(self):
        self.rank_history.append(self.rank_current)
        
    def get_K(self):
        return self.K
      
    def set_K(self, K):
        self.K = K
        
    def add_set(self, tournament, match_set):
        if(tournament not in self.sets):
            self.sets[tournament] = [match_set]
        else:
            self.sets[tournament].append(match_set)
        

class Set(JsonSerializable):
    def __init__(self, winner, loser):
        self.index = None
        self.winner = winner
        self.loser = loser

    def __str__(self):
        return '('+str(self.winner)+", "+str(self.loser)+')'
        
    def set_index(self, idx):
        self.index = idx
    
    def get_index(self):
        return self.index
    
    def get_set(self):
        return (self.winner, self.loser)
    
    def set_winner(self, winner):
        self.winner = winner

    def set_loser(self, loser):
        self.loser = loser

class Tournament(JsonSerializable):
    def __init__(self, name, link, is_ranked):
        self.link = link
        self.name = name
        self.is_ranked = is_ranked
        self.sets = []
    
    def get_name(self):
        return self.name

    def fetch_sets(self, api_key):
        # retrieve a tournament's match list
        payload = {'api_key' : api_key}
        r = requests.get(self.link+'matches.json', params=payload)
        print("retreiving matches from %s"%(r.url))

        for match in r.json():
            # check that this is a bracket match, not part of group stage
            if(match['match']['group_id'] == None):

                winner_id = match['match']['winner_id']
                loser_id = match['match']['loser_id']

                r2 = requests.get(self.link+'participants/%s.json'%(winner_id), params=payload)

                winner_name = r2.json()["participant"]['name']

                r2 = requests.get(self.link+'participants/%s.json'%(loser_id), params=payload)
                loser_name = r2.json()["participant"]['name']

                self.sets.append(Set(winner_name, loser_name))

    def assign_sets(self, sets):
        self.sets = sets

    def get_match(self):
        # retrieve a single match record for a tournament
        pass
 
    def set_status(self, status):
        self.is_ranked = status #status should be boolean
        
    def get_status(self):
        return self.is_ranked

    def get_sets(self):
        return self.sets



class League(JsonSerializable):
    # class containing all players, tournaments, stores and calculates information
    def __init__(self, name):
        self.name = name
        self.players = {}
        self.tournaments = {}
        self.handles = {} #dict of known handles


    def add_player(self, player):
        self.players[player.get_name()] = player
    
    def get_info(self):
        return (self.name, len(self.players), len(self.tournaments))

    def get_players(self):
        return self.players
  
    def get_player(self, name):
        if(name in self.players): return self.players[name]
        else: return None
    
    def add_tournament(self, tournament):
        if(tournament.get_name() not in self.tournaments):
            self.tournaments[tournament.get_name()] = tournament
            return True
        else:
            #tournament already exists
            return False
    
    def get_tournaments(self):
        return self.tournaments
    
    def get_tournament(self, name):
        return self.tournaments[name]
    
    def load(self, filepath):
        f = open(filepath).read()
        data = json.loads(f, encoding='utf-8')
        self.name = data["name"]
        for name, player in data["players"].items():
            self.players[name] = Player(name)
            self.players[name].set_K(player["K"])
            self.players[name].set_rank_current(player["rank_current"])
            self.players[name].set_rank_history(player["rank_history"])

        for name, tournament in data["tournaments"].items():
            is_ranked = tournament["is_ranked"]
            link = tournament["link"]
            name = tournament["name"]
            self.tournaments[name] = Tournament(name, link, is_ranked)
            self.tournaments[name].assign_sets(tournament["sets"])


  
    def preprocess_sets(self):
        # Get mapping of known handles
        handles = self.handles
        
        # Count sets so we have an index of who played and when
        set_count = 0
        
        #Iterate over tournaments to compute player names and then compute score
        for name, tournament in self.tournaments.items():
            # Get the current tournament's sets
            curr_sets = tournament.get_sets()
            
            for curr_set in curr_sets:
            # print set winner and loser and ask user for a name, then add player handle to handle list
                curr_set.set_index(set_count)
                winner, loser = curr_set.get_set()
                if(winner not in handles):
                    w_name = input("Current handle is listed as %s, who is this player? "%(winner))
                    handles[winner] = w_name
                elif(winner in handles):
                    print("%s is already in list of handles! matching to player name: %s"%(winner, handles[winner]))
                    w_name = handles[winner]
            
                if(w_name not in self.players):
                    print("adding %s to league"%(w_name))
                    self.players[w_name] = Player(w_name)

                curr_set.set_winner(w_name)
              
                if(loser not in handles):
                    l_name = input("Current handle is listed as %s, who is this player? "%(loser))
                    handles[loser] = l_name
                elif(loser in handles):
                    l_name = handles[loser]
                    print("%s is already in list of handles! matching to player name: %s"%(loser, handles[loser]))
              
                if(l_name not in self.players):
                    print("adding %s to league"%(l_name))
                    self.players[l_name] = Player(l_name)
                
                curr_set.set_loser(l_name)
                
                curr_set.set_index(set_count)
                
                # increment set count
                set_count+=1
    
                
                
                self.players[w_name].add_set(name, curr_set)
                self.players[l_name].add_set(name, curr_set)

        self.handles = handles
         

    def processRanks(self):
        # iterate through tournaments, calculating
        # ranks of all players
        for name, tournament in self.tournaments.items():
            # Only process tournament if it's ranked
              if(tournament.get_status() == True):
                    # tournament contains sets in form of (winner, loser)
                    current_sets = tournament.get_sets()
                    # check if winner and loser are players in the league
                    for set in current_sets:
                        res = set.get_set()
                        print("Finding players for set: (%s vs %s)"%(res[0], res[1]))
                        winner = self.get_player(res[0])
                        loser = self.get_player(res[1])
                        score_set(winner, loser)
