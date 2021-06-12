'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction, AssignAction
from skeleton.states import GameState, TerminalState, RoundState, BoardState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND, NUM_BOARDS
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot

import eval7
import random
import pandas as pd

class Player(Bot):
    '''
    A pokerbot.
    '''

    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        '''
        self.board_allocation = [[], [], []] # keep track of card allocations at round start
        self.hole_strengths = [0, 0 , 0]
        self.MONTE_CARLO_ITERS = 100

        calculated_df = pd.read_csv('hole_strengths.csv') # all values we made offline
        holes = calculated_df.Holes
        strengths = calculated_df.Strengths
        self.starting_strengths = dict(zip(holes, strengths))

    def hole_list_to_key(self, hole):
        card1, card2 = hole[0], hole[1]
        rank1, suit1 = card1[0], card1[1]
        rank2, suit2 = card2[0], card2[1]

        numeric1, numeric2 = self.rank_to_numeric(rank1), self.rank_to_numeric(rank2)
        suited = suit1 == suit2
        suit_string = 's' if suited else 'o'
        if numeric1 >= numeric2:
            return rank1 + rank2 + suit_string
        else:
            return rank2 + rank1 + suit_string

    def rank_to_numeric(self, rank):
        if rank.isnumeric(): # 2-9
            return int(rank)
        else:
            return [10, 11, 12, 13, 14]['TJQKA'.index(rank)]

    def sort_cards_by_rank(self, cards):
        return sorted(cards, reverse=True, key= lambda x: self.rank_to_numeric(x[0]))
   
    def allocate_cards(self, my_cards):
        # TODO TODO: consider all 6 permutations and allocate, based on precomputed strength 
        # pair-first approach
        ranks = {}
        for card in my_cards:
            card_rank = card[0] # 2-9,T,J,Q,K,A
            # card_suit = card[1] # d,h,s,c
            if card_rank in ranks:
                ranks[card_rank].append(card)
            else:
                ranks[card_rank] = [card]
        
        pairs = []
        singles = []
        for rank in ranks:
            cards = ranks[rank]
            if len(cards) == 1:
                singles.append(cards[0])
            elif len(cards) == 2 or len(cards) == 4:
                pairs += cards
            else: # 3 cards of same rank
                pairs.append(cards[0])
                pairs.append(cards[1])
                singles.append(cards[2])
        
        cards_remaining = set(my_cards) 
        allocated_cards = set()
        holes_allocated = []
        
        _MIN_PAIR_VALUE = 3 # TODO: tune, only want pairs stronger than this value
        for i in range(len(pairs)//2):
            pair = [pairs[2*i], pairs[2*i+1]]
            pair_rank= pair[0][0]
            if self.rank_to_numeric(pair_rank) >= _MIN_PAIR_VALUE:
                holes_allocated.append(pair)
                allocated_cards.update(pair)

        cards_remaining = cards_remaining - allocated_cards
        sorted_remaining = self.sort_cards_by_rank(list(cards_remaining))
        # ADDITION: look for straight cards
        for i in range(len(sorted_remaining) - 1): 
            card_1 = sorted_remaining[i]
            card_2 = sorted_remaining[i+1]
            rank_diff = abs(self.rank_to_numeric(card_1[0]) - self.rank_to_numeric(card_2[0]))
            if (rank_diff <= 1) and (card_1 not in allocated_cards) and (card_2 not in allocated_cards):
                hole = [card_1, card_2]
                holes_allocated.append(hole)
                allocated_cards.update(hole)

        cards_remaining = cards_remaining - allocated_cards
        suits = {}
        # ADDITION: look for flush cards
        for card in cards_remaining: 
            card_suit = card[1]
            if card_suit in suits:
                suits[card_suit].append(card)
            else:
                suits[card_suit] = [card]
        for suit, cards in suits.items():
            if len(cards) in {2, 3}:
                hole = [cards[0], cards[1]]
                holes_allocated.append(hole)
                allocated_cards.update(hole)
            elif len(cards) == 4: # be wary
                a,b,c,d = cards
                hole_1 = [a,b]
                hole_2 = [c,d]
                holes_allocated.append(hole_1)
                allocated_cards.update(hole_1)
                holes_allocated.append(hole_2)
                allocated_cards.update(hole_2)

        cards_remaining = cards_remaining - allocated_cards
        extra_cards = list(cards_remaining)
        for i in range(len(extra_cards) //2):
            hole = [extra_cards[2*i], extra_cards[2*i+1]]
            holes_allocated.append(hole)
            allocated_cards.update(hole)

        cards_remaining = cards_remaining - allocated_cards
        assert len(holes_allocated) == 3, "we allocated too many cards"
        assert len(cards_remaining) == 0, "we have yet allocated all cards"
        return holes_allocated

    # randomizing hole_cards to board
    def assign_holes(self, hole_cards):
        holes_and_strengths = [] 
        for hole in hole_cards:
            key = self.hole_list_to_key(hole)
            strength = self.starting_strengths[key]
            holes_and_strengths.append((hole, strength))
        
        holes_and_strengths = sorted(holes_and_strengths, key = lambda x: x[1])
        # TODO: tune, some random swaps
        board_A, board_B, board_C = holes_and_strengths
        if random.random() < .08: # swap best with second
            holes_and_strengths = [board_A, board_C, board_B]
        board_A, board_B, board_C = holes_and_strengths
        if random.random() < .18: # swap second with worst
            holes_and_strengths = [board_B, board_A, board_C]

        for i in range(NUM_BOARDS):
            self.board_allocation[i] = holes_and_strengths[i][0]
            self.hole_strengths[i] = holes_and_strengths[i][1]

    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        opp_bankroll = game_state.opp_bankroll # ^but for your opponent
        game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        my_cards = round_state.hands[active]  # your six cards at the start of the round
        big_blind = bool(active)  # True if you are the big blind
        
        allocated_holes = self.allocate_cards(my_cards)
        self.assign_holes(allocated_holes)

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        opp_delta = terminal_state.deltas[1-active] # your opponent's bankroll change from this round 
        previous_state = terminal_state.previous_state  # RoundState before payoffs
        street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        for terminal_board_state in previous_state.board_states:
            previous_board_state = terminal_board_state.previous_state
            my_cards = previous_board_state.hands[active]  # your cards
            opp_cards = previous_board_state.hands[1-active]  # opponent's cards or [] if not revealed
        
        self.board_allocation = [[], [], []] 
        self.hole_strengths = [0, 0 , 0]

        game_clock = game_state.game_clock
        round_num = game_state.round_num
        if round_num == NUM_ROUNDS:
            print("time remaining ", game_clock)


    def get_actions(self, game_state, round_state, active):
        '''
        Where the magic happens - your code should implement this function.
        Called any time the engine needs a triplet of actions from your bot.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Your actions.
        '''
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        my_cards = round_state.hands[active]  # your cards across all boards
        board_cards = [board_state.deck if isinstance(board_state, BoardState) else board_state.previous_state.deck \
            for board_state in round_state.board_states] #the board cards
        my_pips = [board_state.pips[active] if isinstance(board_state, BoardState) else 0 \
            for board_state in round_state.board_states] # the number of chips you have contributed to the pot on each board this round of betting
        opp_pips = [board_state.pips[1-active] if isinstance(board_state, BoardState) else 0 for board_state in round_state.board_states] # the number of chips your opponent has contributed to the pot on each board this round of betting
        continue_cost = [opp_pips[i] - my_pips[i] for i in range(NUM_BOARDS)] #the number of chips needed to stay in each board's pot
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        stacks = [my_stack, opp_stack]
        net_upper_raise_bound = round_state.raise_bounds()[1] # max raise across 3 boards
        net_cost = 0 # keep track of the net additional amount you are spending across boards this round
        
        my_actions = [None] * NUM_BOARDS
        for i in range(NUM_BOARDS):
            if AssignAction in legal_actions[i]:
                cards = self.board_allocation[i]
                my_actions[i] = AssignAction(cards)
            elif isinstance(round_state.board_states[i], TerminalState):
                my_actions[i] = CheckAction()
            else: # do we add more resources?
                board_cont_cost = continue_cost[i]
                board_total = round_state.board_states[i].pot
                pot_total = my_pips[i] + opp_pips[i] + board_total
                min_raise, max_raise = round_state.board_states[i].raise_bounds(active, round_state.stacks)
                # TODO TODO: use `street` (0,3,4,5) to get more accurate strength from new cards (turn and river), not just from hole cards
                strength = self.hole_strengths[i] 
                
                if street < 3: # in pre-flop
                    ## TODO: tune bet proportions
                    raise_amount = int(my_pips[i] + board_cont_cost + 0.45 * (pot_total + board_cont_cost))
                else: # turn/ river, deeper in games with stronger hand
                    raise_amount = int(my_pips[i] + board_cont_cost + 0.84 * (pot_total + board_cont_cost))
                
                raise_amount = max(min_raise, raise_amount)
                raise_amount = min(max_raise, raise_amount)

                raise_cost = raise_amount - my_pips[i]
                if RaiseAction in legal_actions[i] and (raise_cost <= my_stack - net_cost):
                    commit_action = RaiseAction(raise_amount)
                    commit_cost = raise_cost
                elif CallAction in legal_actions[i]:
                    commit_action = CallAction()
                    commit_cost = board_cont_cost
                else:
                    commit_action = CheckAction()
                    commit_cost = 0
                
                if board_cont_cost > 0: # our opp raised!
                    if board_cont_cost > 4:
                        _THREAT = 0.17
                        strength = max(0, strength - _THREAT)
                    pot_odds = board_cont_cost / (pot_total + board_cont_cost)
                    if strength >= pot_odds: # +ExpValue: at least call
                        if strength > 0.59 and strength> random.random():
                            my_actions[i] = commit_action
                            net_cost += commit_cost
                        else:
                            my_actions[i] = CallAction()
                            net_cost += board_cont_cost
                    else: # -EV: FOLD!
                        my_actions[i] = FoldAction()
                        net_cost += 0
                else: # board_cont_cost == 0
                    if strength > random.random():
                        my_actions[i] = commit_action
                        net_cost += commit_cost
                    else: 
                        my_actions[i] = CheckAction()
                        net_cost += 0
                    
        return my_actions


if __name__ == '__main__':
    run_bot(Player(), parse_args())
