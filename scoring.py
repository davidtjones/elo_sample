def elo_score_set(winner, loser, classification, update=True):
    if(classification == 'M'):
        K_divisor = .5
    else:
        K_divisor = 1
    if((winner.get_rank_current()) == None): winner.set_rank_current(1200)
    if((loser.get_rank_current()) == None): loser.set_rank_current(1200)
    
    P1 = (1.0 / (1.0 + (10**((loser.get_rank_current() - winner.get_rank_current())/400))))
    P2 = (1.0 / (1.0 + (10**((winner.get_rank_current() - loser.get_rank_current())/400))))
    
    #choose lowest K
    low_K = winner.get_K() if winner.get_K() <= loser.get_K() else loser.get_K()
    
    w_new_rank = winner.get_rank_current() + (low_K*K_divisor) * (1 - P1)
    l_new_rank = loser.get_rank_current() + (low_K*K_divisor) * (0 - P2)
    
    if(update== True):
        winner.set_rank_current(w_new_rank)
        loser.set_rank_current(l_new_rank)
    
    return (w_new_rank, l_new_rank)

def elo_sort(players):
    plist = []
    for name, player in players.items():
        plist.append((name, player.get_rank_current()))

    #filter none types
    plist_f = list(filter(lambda x: x[1] != None, plist))

    #sort remainder of list
    plist_s = sorted(plist_f, key=lambda x: x[1], reverse=True)
    return plist_s

def processDecay(player_d, players, decay, delay=1):
    # delay = 1
    total = 0
    print("processing decay for %s"%(player_d.get_name()))
    for name, player in players.items():
        w, l = elo_score_set(player, player_d, update=False)
        total += (w - player.get_rank_current())
    
    for name, player in players.items():
        if(player_d.get_name() != name):
            slice_d = decay/total
            w, l = elo_score_set(player, player_d, update=False)
            player.set_rank_current(player.get_rank_current() + (slice_d * (w-player.get_rank_current())))
        
    player_d.set_rank_current(player_d.get_rank_current() - decay)
 
       
