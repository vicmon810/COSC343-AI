#Import stuff
from cosc343TicTacToe import maxs_possible_moves,\
                                mins_possible_moves,\
                                terminal, evaluate, \
                                state_change_to_action, \
                                remove_symmetries
import numpy as np

#My agent class
class TicTacToeAgent():
    """
           A class that encapsulates the code dictating the
           behaviour of the TicTacToe playing agent

           Methods
           -------
           AgentFunction(percepts)
               Returns the move made by the agent given state of the game in percepts
           """

    def __init__(self, h):
        """Initialises the agent

        :param h: Handle to the figures showing state of the board -- only used
                  for human_agent.py to enable selecting next move by clicking
                  on the matplotlib figure.
        """
        pass

    # Implement minimax algorithm here
    def Minimax(self, state, depth, maximising):
        #Base case
        if depth == 0 or terminal(state):
            return evaluate(state), state
        #Set max or min states
        if maximising:
            #Score to compare so that algorithm wouldn't just take the best value
            checkscore = -101
            checkmove = None
            #Get possible states
            new_states = remove_symmetries(maxs_possible_moves(state))
            #For each possible states
            for s in new_states:
                #Recursive function
                score,state = self.Minimax(s, depth - 1, False)
                #Final check to make sure that other options are considered
                if (checkscore < score):
                    checkscore = score
                    checkmove = s
            return checkscore,checkmove #Return value
        else: #If min
            #Score to compare so that algorithm wouldn't pick worst min value
            checkscore = 101
            checkmove = None
            #Get possible min states
            new_states = remove_symmetries(mins_possible_moves(state))
            #For each state
            for s in new_states:
                #Recursive statement
                score, state = self.Minimax(s, depth - 1, True)
                #Final check to make sure that other options are considered
                if (checkscore > score):
                    checkscore = score
                    checkmove = s
            return checkscore, checkmove

    # r is row, c is col, percepts is 2D list of positions of current agent
    #Agent Function
    def AgentFunction(self, percepts):
        #Current state
        states = percepts
        #Run minimax algorithm
        score,new_state = self.Minimax(states, 9, True)
        #Get row and column value
        r,c = state_change_to_action(percepts, new_state)
        return (r,c)