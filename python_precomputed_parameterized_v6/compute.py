import eval7
import itertools
import pandas as pd

def calculate_strength(hole, iters): # Kd, 9h,...
    # calculate strength for different hand (pair) of holes
    deck = eval7.Deck() # eval7 object (52-card Deck) -- copy Deck (a list)
    hole_cards = [eval7.Card(card) for card in hole]
    for card in hole_cards:
        deck.cards.remove(card) # remove elm from Deck (a list) = slow

    # Monte Carlo simulation - to approx hand strength
    # TODO: runtime bottleneck
    score = 0
    for _ in range(iters): # O(iters) = bottleneck
        deck.shuffle() # Python: Fisher-Yates shuffle algorithm O(num_cards)

        _COMM, _OPP = 5, 2

        draw = deck.peek(_COMM + _OPP)
        community = draw[_OPP: ]
        opp_hand = draw[: _OPP] + community
        our_hand = hole_cards + community
        # compare hands
        our_hand_value = eval7.evaluate(our_hand)
        opp_hand_value = eval7.evaluate(opp_hand)
        _WIN_SCORE = 1
        if  our_hand_value > opp_hand_value :  # win
            score += _WIN_SCORE
        elif our_hand_value == opp_hand_value:  # tie
            score += _WIN_SCORE/2
        else: # lost 
            score += 0

    return score / iters

if __name__ == "__main__":
    _MONTE_CARLO_ITERS = 345000 # 
    _RANKS = 'AKQJT98765432'

    off_rank_holes = list(itertools.combinations(_RANKS, 2)) # all holes, except pocket pairs (AA, KK, QQ,..)
    pocket_pairs_holes = list(zip(_RANKS, _RANKS))

    # suited (Ad, Kd) = AKs;; off-suited (Ad, Ks) = AKo
    suited_strenghts = [round(calculate_strength([hole[0] + 'c', hole[1] + 'c'], _MONTE_CARLO_ITERS), 5) \
        for hole in off_rank_holes] # all holes with same suit
    off_suited_strenghts = [round(calculate_strength([hole[0] + 'c', hole[1] + 'd'], _MONTE_CARLO_ITERS), 5) \
        for hole in off_rank_holes] # all holes with off suit
    pocket_pairs_strengths = [round(calculate_strength([hole[0] + 'c', hole[1] + 'd'], _MONTE_CARLO_ITERS), 5) \
        for hole in pocket_pairs_holes] # also off suit, from pocket pairs

    suited_holes = [hole[0] + hole[1] + 's' for hole in off_rank_holes]
    off_suited_holes = [hole[0] + hole[1] + 'o' for hole in off_rank_holes]
    pocket_pairs = [hole[0] + hole[1] + 'o' for hole in pocket_pairs_holes]

    all_strengths = suited_strenghts + off_suited_strenghts + pocket_pairs_strengths
    all_holes = suited_holes + off_suited_holes + pocket_pairs

    hole_df = pd.DataFrame()
    hole_df['Holes'] = all_holes
    hole_df['Strengths'] = all_strengths

    hole_df.to_csv('hole_strengths.csv', index=False)


    