k = 100

from tabulate import tabulate
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

names = [   
      "David",
      "Jacob",
      "Skyler",
      "Lee",
      "Benton",
      "Adam",
      "Calvin",
      "Crystal",
      "Zane",
      "Hayden",
      "Drew",
      "Steve",
      "Kent",
      "Landon",
      "Greg",
      "Conner"
  ]

class Player:
    def __init__(self, name):
        self.name = name
        self.rank = None # no score if the player hasn't played a ranked match yet
        
    def __str__(self):
        return self.name
        
    def set_rank(self, num):
        self.rank = num
    
    def get_rank(self):
        return self.rank
        

def score_set(player1, player2, winner):
  # computes the new ELO of two players - this function will handle all 
  # the elo heavy-lifting
  
  # If players aren't ranked currently, they are now :)
  
  if(player1.get_rank() == None):
    player1.set_rank(1200)
  if(player2.get_rank() == None):
    player2.set_rank(1200)
    
  #winner = 1 if player 1 wins, 2 if player 2 wins

  P1 = (1.0 / (1.0 + (10**((player2.get_rank() - player1.get_rank())/400))))
  P2 = (1.0 / (1.0 + (10**((player1.get_rank() - player2.get_rank())/400))))

  #print("Probability of %s winning: %s"%(player1, P1))
  #print("Probability of %s winning: %s"%(player2, P2))

  #print("Obviously, these add up to 1.0: %s + %s = %s"%(P1, P2, P1+P2))

  #print("The rating of the player who wins is updated")
  #print("If Skyler wins:")

  if(winner == 1):
    p1_new_rank = player1.get_rank() + k * (1 - P1)
    p2_new_rank = player2.get_rank() + k * (0 - P2)
  elif(winner == 2):
    p1_new_rank = player1.get_rank() + k * (0 - P1)
    p2_new_rank = player2.get_rank() + k * (1 - P2)
  else:
    print("there's a problem dawg")

  player1.set_rank(p1_new_rank)
  player2.set_rank(p2_new_rank)

  #print("New ELO Scores: Benton (%s), Skyler (%s):"%(player1.get_rank(), player2.get_rank()))
 
  return

def computeranks(tournaments):


  #Create a dictionary with the names using the Player class
  players = {}
  for name in names:
    players[name] = Player(name)


  if ("SB1" in tournaments and tournaments["SB1"]):
    #logic to pull tournament data
    score_set(players["David"], players["Calvin"], 1)
    score_set(players["Zane"], players["Calvin"], 2)
    score_set(players["David"], players["Greg"], 1)
    score_set(players["Greg"], players["Calvin"], 1)
    score_set(players["David"], players["Lee"], 2)
    score_set(players["David"], players["Lee"], 2)

  if("SB2" in tournaments and tournaments["SB2"]):
    #logic to pull tournament data
    score_set(players["David"], players["Zane"], 1)
    score_set(players["Lee"], players["Calvin"], 1)
    score_set(players["Zane"], players["Calvin"], 2)
    score_set(players["David"], players["Lee"], 2)
    score_set(players["David"], players["Crystal"], 1)
    score_set(players["Calvin"], players["David"], 2)
    score_set(players["Lee"], players["David"], 1)

  if("SB3" in tournaments and tournaments["SB3"]):
    #logic to pull tournament data
    score_set(players["Greg"], players["David"], 2)
    score_set(players["Calvin"], players["Jacob"], 2)
    score_set(players["Lee"], players["Zane"], 1)
    score_set(players["Greg"], players["Calvin"], 1)
    score_set(players["Lee"], players["David"], 1)
    score_set(players["David"], players["Jacob"], 1)
    score_set(players["David"], players["Jacob"], 2)
    score_set(players["Benton"], players["Lee"], 2)
    score_set(players["Benton"], players["Greg"], 1)
    score_set(players["Jacob"], players["Zane"], 1)
    score_set(players["Benton"], players["Jacob"], 2)
    score_set(players["David"], players["Lee"], 2)
    score_set(players["Lee"], players["Jacob"], 1)

  if("SB4" in tournaments and tournaments["SB4"]):
    #logic to pull tournament data
    score_set(players["Benton"], players["David"], 1)
    score_set(players["Zane"], players["Hayden"], 1)
    score_set(players["Crystal"], players["Greg"], 2)
    score_set(players["Hayden"], players["Crystal"], 1)
    score_set(players["Skyler"], players["Benton"], 1)
    score_set(players["Greg"], players["Zane"], 2)
    score_set(players["David"], players["Greg"], 1)
    score_set(players["Hayden"], players["Benton"], 2)
    score_set(players["Skyler"], players["Zane"], 1)
    score_set(players["David"], players["Benton"], 1)
    score_set(players["David"], players["Zane"], 1)
    score_set(players["David"], players["Skyler"], 2)


  if("C1" in tournaments and tournaments["C1"]):
    #logic to pull tournament data
    score_set(players["Crystal"], players["Greg"], 1)
    score_set(players["Skyler"], players["Drew"], 1)
    score_set(players["Calvin"], players["Hayden"], 1)
    score_set(players["David"], players["Steve"], 1)
    score_set(players["Benton"], players["Conner"], 1)
    score_set(players["Hayden"], players["Drew"], 1)
    score_set(players["Lee"], players["Crystal"], 1)
    score_set(players["Jacob"], players["Benton"], 1)
    score_set(players["Skyler"], players["Calvin"], 1)
    score_set(players["David"], players["Zane"], 1)
    score_set(players["Steve"], players["Crystal"], 1)
    score_set(players["Zane"], players["Greg"], 1)
    score_set(players["Hayden"], players["Steve"], 1)
    score_set(players["Calvin"], players["Zane"], 1)
    score_set(players["Lee"], players["Jacob"], 1)
    score_set(players["Skyler"], players["David"], 1)
    score_set(players["Jacob"], players["Calvin"], 1)
    score_set(players["David"], players["Hayden"], 1)
    score_set(players["Skyler"], players["Lee"], 1)
    score_set(players["Jacob"], players["David"], 1)
    score_set(players["Jacob"], players["Lee"], 1)
    score_set(players["Skyler"], players["Jacob"], 1)

  if("C2" in tournaments and tournaments["C2"]):
    #logic to pull tournament data
    score_set(players["Drew"], players["Crystal"], 2)
    score_set(players["Benton"], players["Conner"], 1)
    score_set(players["Lee"], players["Benton"], 1)
    score_set(players["Jacob"], players["Zane"], 1)
    score_set(players["Calvin"], players["Crystal"], 1)
    score_set(players["Zane"], players["Drew"], 1)
    score_set(players["Benton"], players["Zane"], 1)
    score_set(players["David"], players["Skyler"], 2)
    score_set(players["Benton"], players["David"], 1)
    score_set(players["Lee"], players["Jacob"], 1)
    score_set(players["Benton"], players["Jacob"], 2)
    score_set(players["Lee"], players["Skyler"], 1)
    score_set(players["Skyler"], players["Jacob"], 1)
    score_set(players["Lee"], players["Skyler"], 2)
    score_set(players["Lee"], players["Skyler"], 2)

  if("Cinco" in tournaments and tournaments["Cinco"]):
     #logic to pull tournament data
      score_set(players["David"], players["Zane"], 1)
      score_set(players["Benton"], players["Landon"], 1)
      score_set(players["Crystal"], players["Kent"], 1)
      score_set(players["Lee"], players["Adam"], 1)
      score_set(players["Landon"], players["Zane"], 1)
      score_set(players["Adam"], players["Kent"], 1)
      score_set(players["Benton"], players["David"], 1)
      score_set(players["Lee"], players["Crystal"], 1)
      score_set(players["Landon"], players["Crystal"], 1)
      score_set(players["David"], players["Adam"], 1)
      score_set(players["David"], players["Landon"], 1)
      score_set(players["Benton"], players["Lee"], 1)
      score_set(players["David"], players["Lee"], 1)
      score_set(players["Benton"], players["David"], 1)


  if("C3" in tournaments and tournaments["C3"]):
    #logic to pull tournament data
    score_set(players["Crystal"], players["Zane"], 1)
    score_set(players["Benton"], players["Drew"], 1)
    score_set(players["Calvin"], players["Kent"], 1)
    score_set(players["Adam"], players["Hayden"], 1)
    score_set(players["Landon"], players["Steve"], 1)
    score_set(players["Kent"], players["Drew"], 1)
    score_set(players["Crystal"], players["Lee"], 1)
    score_set(players["Benton"], players["Calvin"], 1)
    score_set(players["Adam"], players["Jacob"], 1)
    score_set(players["David"], players["Landon"], 1)
    score_set(players["Jacob"], players["Kent"], 1)
    score_set(players["Lee"], players["Steve"], 1)
    score_set(players["Landon"], players["Zane"], 1)
    score_set(players["Calvin"], players["Hayden"], 1)
    score_set(players["Jacob"], players["Landon"], 1)
    score_set(players["Lee"], players["Calvin"], 1)
    score_set(players["Benton"], players["Crystal"], 1)
    score_set(players["David"], players["Adam"], 1)
    score_set(players["Jacob"], players["Crystal"], 1)
    score_set(players["Adam"], players["Lee"], 1)
    score_set(players["Adam"], players["Jacob"], 1)
    score_set(players["David"], players["Benton"], 1)
    score_set(players["David"], players["Adam"], 1)
  
  # get a list of players and their scores:
  rankings = []
  for key, value in players.items():
    rankings.append((str(value), value.get_rank()))

  return rankings
  
  
def elo_sort(rankings):
  # pass in a list of (name, rank) to output an ordered list with 'None' ranks excluded
  
  #filter none types
  #list(filter((None).__ne__, rankings))
  rankings = list(filter(lambda x: x[1] != None, rankings))
  #print(rankings)
  
  #sort remainder of list
  rankings_sorted = sorted(rankings, key=lambda x: x[1], reverse=True)
  
  return rankings_sorted
    

# Change these to 0 if you don't want them included or 1 if you do want them included :)
tournaments = {
      "SB1" : 1,
      "SB2" : 1,
      "SB3" : 1,
      "SB4" : 1,
      "C1"  : 1,
      "C2"  : 1,
      "Cinco" : 1,
      "C3":  1
}


rankings = computeranks(tournaments)

rs = elo_sort(rankings)

print(tabulate(rs, showindex=True))

sb1 = { "SB1" : 1}
sb2 = { "SB1" : 1, "SB2" : 1}
sb3 = { "SB1" : 1, "SB2" : 1, "SB3" : 1}
sb4 = { "SB1" : 1, "SB2" : 1, "SB3" : 1, "SB4" : 1}
c1 = { "SB1" : 1, "SB2" : 1, "SB3" : 1, "SB4" : 1, "C1" : 1}
c2 = { "SB1" : 1, "SB2" : 1, "SB3" : 1, "SB4" : 1, "C1" : 1, "C2" : 1}
cinco = { "SB1" : 1, "SB2" : 1, "SB3" : 1, "SB4" : 1, "C1" : 1, "C2" : 1, "Cinco" : 1}
c3 = { "SB1" : 1, "SB2" : 1, "SB3" : 1, "SB4" : 1, "C1" : 1, "C2" : 1, "Cinco" : 1, "C3" : 1}

rankings_sb1 = computeranks(sb1)
rankings_sb2 = computeranks(sb2)
rankings_sb3 = computeranks(sb3)
rankings_sb4 = computeranks(sb4)
rankings_c1 = computeranks(c1)
rankings_c2 = computeranks(c2)
rankings_cinco = computeranks(cinco)
rankings_c3 = computeranks(c3)
rankings_ot = []
for i in range(len(rankings_sb1)):
  rankings_ot.append([rankings_sb1[i][0], rankings_sb1[i][1], rankings_sb2[i][1], rankings_sb3[i][1], rankings_sb4[i][1], rankings_c1[i][1], rankings_c2[i][1], rankings_cinco[i][1], rankings_c3[i][1]])


print(tabulate(rankings_ot, headers = ['Name', 'SB1', 'SB2', 'SB3', 'SB4', 'Clash 1', 'Clash 2', 'Cinco', 'Clash 3']))


# Create plots for model training data
x = np.arange(1, 9)

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
colormap = plt.cm.nipy_spectral

colors = plt.cm.Spectral(np.linspace(0,1,16))
ax1.set_prop_cycle('color', colors)

for i in range(len(rankings_ot)):
  ax1.plot(x, rankings_ot[i][1:], label=rankings_ot[i][0])

box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])

plt.xticks(x, ('SB1', 'SB2', 'SB3', 'SB4', 'C1', 'C2', 'Cinco', 'C3'))
ax1.legend(loc='center left', bbox_to_anchor=(1, .5),
          ncol=1, fancybox=True, shadow=True)
#plt.show()

fig1.savefig('elo.png', dpi = 300)