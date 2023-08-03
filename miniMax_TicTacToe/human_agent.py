__author__ = "Lech Szymanski"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "lech.szymanski@otago.ac.nz"

# Import the random number generation library
import time
import numpy as np
import matplotlib.pyplot as plt


# Create a subclass of tictactoe with an implementation of
# the agent_move function
class TicTacToeAgent():

    def __init__(self,h):
        self.h = h

    def __call__(self, event):
        if event.xdata is None or event.ydata is None:
            return

        c = int(np.floor(event.xdata))
        r = 2 - int(np.floor(event.ydata))

        if self.state[r][c] == 0:
          self.r = r
          self.c = c
          self.h.figure.canvas.mpl_disconnect(self.cid)
          self.ready = True
          plt.ion()

    # The agent_move function - the function has to tell the
    # tictactoe class what move to make next in the game
    #
    # Inputs: state - current state of the board
    # Returns: new state of the board with the proposed move
    def AgentFunction(self, percepts):

        self.ready = False
        self.state = percepts
        self.cid = self.h.figure.canvas.mpl_connect('button_press_event', self)


        while not self.ready:
            plt.draw()
            plt.pause(0.01)
            time.sleep(0.01)

        return (self.r,self.c)


