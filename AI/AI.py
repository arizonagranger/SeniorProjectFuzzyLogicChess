# written by Haley Granger
# Senior Project AI Chess

# Monte Carlo Tree Search

import requests
import datetime
from random import choice
from math import log, sqrt

#rules engine url
URL = "http://localhost:4850/"

class Board(object):
    def new_game():
    #initialize new board and new game state
        newGame = requests.get(url = URL + "new-game")
        board = requests.get(url = URL + "game-state")

        chessAI = MonteCarlo(board)
    
    def save_state(board):
        save = requests.post(url = URL + "save-state")
        pop = requests.post(url = URL + "restore-state")



print(board.text)

class MonteCarlo(object):
    #instance of a board and takes some optional arguments
    def __init__(self, board, **kwargs):
        self.board = board
        self.states = []
        self.max_moves = kwargs.get('max_moves', 100)
        
        self.wins = {}
        self.plays = {}

        self.C = kwargs.get('C', 1.4)


"""
    # appends gamestate to stack in RulesEngine
    def update(self, state):
        self.states.append(state)

    #chooses best move from current game state
    def best_move(self):
        #to track calculation times
        start = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - start < self.calculation_time:
            self.simulation()

    #runs a simulation of game from current node position
    def simulation(self):
        plays, wins = self.plays, self.wins
        visited_states = set()
        states_copy = self.states[:]
        state = states_copy[-1]
        player = self.board.current_player(state)
        
        expand = True

        for t in xrange(1, self.max_moves+ 1):
            legal = self.board.legal_plays(states_copy)
            moves_states = [(p, self.boar.next_state(state,p)) for p in legal]

            if all(plays.get((player, S)) for p, S in moves_states):
                log_total = log(sum(plays[(player, S)] for p, S in moves_States))
                value, move, state = max(((wins[(player,S)]/plays[(player, S)})                      + self.C * sqrt(log_total/plays[(player, S)]), p, S)
                        for p, S in moves_states
                    )
            else:
                move, state = choice(moves_states)

            states_copy.append(state)

            play = choice(legal)
            
            if expand and (player, State) not in plays:
                expand = False
                plays[(player, state)] = 0
                wins [ (player, state)] = 0
                if t > self.max_depth:
                    self.max_depth = t
            visited_states.add((player, state))

            player = self.board.current_player(state)
            
            state = self.board.next_state(state, play)
            states_copy.append(state)
            winner = self.board.winner(states_copy)
            
            if winner:
                break

        for player, state in visited_states:
            if(player, state) not in plays:
                continue
            plays[(player, state)] += 1
            if player == winner:
                wins[(player, state)] += 1


"""
