import requests
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import json
import pickle

from scoring import elo_score_set, processDecay
from config import api_key

# Class Definitions
class JsonSerializable():
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

    def __repr__(self):
        return self.toJSON()


class Player(JsonSerializable):
    def __init__(self, name):
        self.index = None
        self.name = name
        self.rank_current = None
        self.rank_history = [] # no score if the player hasn't played a ranked match yet
        #self.handles = []
        self.K = 10
        self.is_ranked = True
        self.sets = []

    def __str__(self):
        return self.name
    
    def set_index(self, index):
        self.index = index

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

    def get_rank_status(self):
        return self.is_ranked

    def add_set(self, match):
        self.sets.append(match)

    def set_rank_status(self, status):
        if(type(status) is bool):
            self.is_ranked = status
            return 1
        else:
            return 0
    
    def assign_sets(self, sets):
        self.sets = sets

class Set(JsonSerializable):
    def __init__(self, winner, loser):
        self.index = None
        self.dq = False
        self.winner = winner
        self.loser = loser
        
    
    def __str__(self):
        return '('+str(self.winner)+", "+str(self.loser)+')'
        
    def set_index(self, idx):
        #dangerous, be careful using this
        self.index = idx
    
    def get_index(self):
        return self.index
    
    def get_set(self):
        return (self.winner, self.loser)
    
    def get_set_id(self):
        return self.index
    
    def set_winner(self, winner):
        self.winner = winner

    def set_loser(self, loser):
        self.loser = loser
        
    def is_dq(self):
        return self.dq

    def set_dq(self, dq):
        self.dq = dq

class Tournament(JsonSerializable):
    def __init__(self, name, link, is_ranked):
        self.link = link
        self.name = name
        self.is_ranked = is_ranked
        self.sets = []
        self.attendies = []

    
    def get_name(self):
        return self.name

    def fetch_sets(self, api_key, show_key=False):
        raw_matches = []
        # retrieve a tournament's match list
        payload = {'api_key' : api_key}
        r = requests.get(self.link+'matches.json', params=payload)
        
        if(not show_key): print("Retreiving matches from %s..."%(r.url[:(len(r.url) - (len(api_key)-5))]))
        else: print("Retreiving matches from %s"%(r.url))

        for match in r.json():
            # check that this is a bracket match, not part of group stage
            if(match['match']['group_id'] == None):

                winner_id = match['match']['winner_id']
                loser_id = match['match']['loser_id']

                r2 = requests.get(self.link+'participants/%s.json'%(winner_id), params=payload)

                winner_name = r2.json()["participant"]['name']

                r2 = requests.get(self.link+'participants/%s.json'%(loser_id), params=payload)
                loser_name = r2.json()["participant"]['name']

                raw_matches.append((winner_name, loser_name))

        return raw_matches

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

    def add_set(self, match):
        self.sets.append(match)

    def assign_sets(self, sets):
        self.sets = sets

    def remove_set(self, match):
        del self.sets[match]
    
    def add_attendie(self, attendie):
        if(attendie not in self.attendies):
            self.attendies.append(attendie)
        
    def get_attendies(self):
        return self.attendies
        



class League(JsonSerializable):
    # class containing all players, tournaments, stores and calculates information
    def __init__(self, name, events):

        self.name = name # string
        self.events = events # dictionary {name: api_event_link} or None if planning to load from file
        self.players = {}
        self.player_count = 0
        self.tournaments = {}
        self.sets = []
        self.set_count = 0
        self.event_keys_ordered = []

        #self.handles = {} #dict of known handles
        self.handles = {
            "SmashMaster (Lee Cook, Reigning Champ)": "Lee",
            "C Kizzle (Calvin Keats)": "Calvin",
            "Singed (David Jones)": "David",
            "InZane (Zane Dixon)": "Zane",
            "Wolfe (Mike Wolfe)": "Mike",
            "Dash (John Morton)": "Jon",
            "McClassy (Boone McClaskey)": "Boone",
            "BellatrixRayn (Crystal Cook)": "Crystal",
            "Skyler": "Skyler",
            "Mishi": "Mishi",
            "Benton": "Benton",
            "David": "David",
            "Zane": "Zane",
            "Shakey": "Hayden",
            "Greg": "Greg",
            "Crystal": "Crystal",
            "Lee (Zero Annihilated)": "Lee",
            "Mike (Wolfe)": "Mike",
            "Crystal (BellatrixRayne)": "Crystal",
            "Greg (Duckpond)": "Greg",
            "Jacob (Shaman)": "Jacob",
            "Adam (Umopapisdn)": "Adam",
            "Benton (ScrubbyDoo)": "Benton",
            "Conner": "Conner",
            "Skyler (Gotshun)": "Skyler",
            "Drew (Laoss)": "Drew",
            "Calvin (Krohnos)": "Calvin",
            "Hayden (ShakyCheese)": "Hayden",
            "David (Prophet)": "David",
            "Steven (Rook)": "Steven",
            "Zane (VengefulFenix)": "Zane",
            "Dave (Sub-Zero)": "Dave",
            "Drew": "Drew",
            "Calvin": "Calvin",
            "Lee": "Lee",
            "Jacob": "Jacob",
            "Prophet": "David",
            "": "Zane",
            "Scubbydoo": "Benton",
            "Lando": "Landon",
            "Kentwo.0": "Kent",
            "umo": "Adam",
            "Salty Girl (Bellatrix)": "Crystal",
            "Scrub": "Benton",
            "Laoss": "Drew",
            "Krohnos": "Calvin",
            "Kentwo": "Kent",
            "Umo": "Adam",
            "Shaky Cheese": "Hayden",
            "Steve": "Steven",
            "Leethal": "Lee",
            "Shaman": "Jacob",
            "Kent": "Kent",
            "Drewplet": "Drew",
            "Sorks": "Ross",
            "Duckpond": "Greg",
            "BellatrixRayne": "Crystal",
            "ScrubbyDoo": "Benton"}
            
        if(events is not None):
            # Generate from API
            print("Generating via API")
            for name, data in self.events.items():
                if(events[name][0] != None):
                    self.event_keys_ordered.append(name)
                    t = Tournament(name, data[0], data[1])
                    res = self.add_tournament(t)
                    if (res ==  True):
                        raw_sets = t.fetch_sets(api_key)
                        print("total number of sets in %s: %s"%(name, len(raw_sets)))
                        self.preprocess_sets(t, raw_sets)

    def get_info(self):
        return (self.name, len(self.players), len(self.tournaments), len(self.sets))

    def add_player(self, player):
        player.set_index(self.player_count)
        self.players[player.get_name()] = player
        self.player_count += 1

    def get_player(self, name):
        if(name in self.players): return self.players[name]
        else: return None

    def get_players(self):
        return self.players

    def remove_player(self, player):
        # accepts a player key
        del self.players[player]

    def add_set(self, match):
        match.set_index(self.set_count)
        self.sets.append(match)
        self.set_count += 1

    def get_set(self, match):
        # accepts a set index
        return self.sets[match]

    def get_sets(self):
        return self.sets

    def remove_set(self, match):
        # accepts a set index
        del self.sets[match]
    
    def add_tournament(self, tournament):
        if(tournament.get_name() not in self.tournaments):
            self.tournaments[tournament.get_name()] = tournament
            return True
        else:
            #tournament already exists
            return False
   
    def get_tournament(self, name):
        return self.tournaments[name]

    def get_tournaments(self):
        return self.tournaments
    
    def save(self, path):
        f = open(path, 'w', encoding='utf8')
        f.write(self.toJSON())
        f.close()


    def load(self, filepath):
        f = open(filepath).read()
        data = json.loads(f, encoding='utf-8')
        self.name = data["name"]
        self.handles = data["handles"]
        
        self.events = data['events']
        self.event_keys_ordered = data["event_keys_ordered"]
        self.player_count = data['player_count']
        self.set_count = data['set_count']

        
        for name, player in data["players"].items():
            self.players[name] = Player(name)
            self.players[name].set_index(player['index'])
            self.players[name].set_K(player["K"])
            self.players[name].set_rank_current(player["rank_current"])
            self.players[name].set_rank_history(player["rank_history"])
            self.players[name].set_rank_status(player['is_ranked'])
            self.players[name].assign_sets(player['sets'])
        
        for name, tournament in data["tournaments"].items():
            is_ranked = tournament["is_ranked"]
            link = tournament["link"]
            name = tournament["name"]
            self.tournaments[name] = Tournament(name, link, is_ranked)
            self.tournaments[name].assign_sets(tournament["sets"])
            self.attendies = tournament["attendies"]

        for item in data["sets"]:
            loaded_set = Set(item['winner'], item['loser'])
            loaded_set.set_dq(item['dq'])
            loaded_set.set_index(item['index'])
            self.sets.append(loaded_set)


    def preprocess_sets(self, tournament, raw_matches):
        # Get mapping of known handles
        handles = self.handles
        #print(len(handles))
        
        # get tournament name
        name = tournament.get_name()

        for curr_set in raw_matches:
            # curr_set is of the form (winner, loser)
            # print set winner and loser and ask user for a name, then add player handle to handle list
            winner, loser = curr_set

            # Handle winner name
            if(winner not in handles):
                w_name = input("Current handle is listed as %s, who is this player? "%(winner))
                handles[winner] = w_name
            elif(winner in handles):
                #print("%s is already in list of handles! matching to player name: %s"%(winner, handles[winner]))
                w_name = handles[winner]
        
            if(w_name not in self.players):
                print("adding %s to league"%(w_name))
                self.players[w_name] = Player(w_name)

            # Handle loser name
            if(loser not in handles):
                l_name = input("Current handle is listed as %s, who is this player? "%(loser))
                handles[loser] = l_name
            elif(loser in handles):
                l_name = handles[loser]
                print("%s is already in list of handles! matching to player name: %s"%(loser, handles[loser]))
          
            if(l_name not in self.players):
                print("adding %s to league"%(l_name))
                self.players[l_name] = Player(l_name)
            
            # Create set from scraped data
            finalized_set = Set(w_name, l_name)

            # Register this set with the league to generate set id
            self.add_set(finalized_set)

            # Update classes with set information
            self.players[w_name].add_set(finalized_set.get_set_id())
            self.players[l_name].add_set(finalized_set.get_set_id())
            
            tournament.add_attendie(w_name)
            tournament.add_attendie(l_name)
            tournament.add_set(finalized_set.get_set_id())

        self.handles = handles

    def processRanks(self, decay_val, method='elo', decay=True, delay=1, decay_monthlies=False):
        # process ranks via selected scoring method
        # apply decay via decay params
        # assign ranks and commit them to player rank histories

        set_of_all_players = set()
        for player_name in self.players:
            set_of_all_players.add(player_name)
        
        print("Here are all the players in the set")
        print(set_of_all_players)
        players_being_decayed = set()

        # Rank all players and decay players who are slated for decay
        do_decay = False
        for index, t in enumerate(self.tournaments):
            # determine if decay needs to occur:
            print(index, delay, decay)
            if(index >= delay - 1 and decay):
             # acquire list of participants slated for decay
                print("time to do decay :D")
                do_decay = True
                prev_tourney_sets = []
                
                print("Attendie list for players not being decayed:")
                for i in range(delay):
                    # need the previous $delay tournaments (index, index - 1, index - 2)
                    prev_tourney_attendies.append(set(self.tournaments[self.event_keys_ordered[index - i]].get_attendies()))
                print(prev_tourney_attendies)
                exit()

                players_not_being_decayed = set()
                print("wtf")
                for tourney in prev_tourney_sets:
                    players_not_being_decayed =  players_not_being_decayed.intersection(tourney)
                print("players not being decayed:")
                print(players_not_being_decayed)
                players_being_decayed = set_of_all_players - players_not_being_decayed


            t_sets = self.tournaments[t].get_sets() #list of set indices for given tournament

            for current_set in t_sets:
                # get winner and loser from set id
                winner, loser = self.sets[current_set].get_set()

                #score winner and loser and apply new ranks, unless match is DQ
                if(self.sets[current_set].is_dq() == False):
                    elo_score_set(self.players[winner], self.players[loser])

            # apply decay now that tournament has finished
            if(do_decay):
                print("players being decayed for %s:"%(self.tournaments[t].get_name()))
                for player in players_being_decayed:
                    processDecay(self.get_player(player), self.players, decay)
                    do_decay = False
            


            for name, player in self.players.items():
                player.commit_rank()
              
                



















































































































































































































































































































































































































































































































































































































































































































































































































































