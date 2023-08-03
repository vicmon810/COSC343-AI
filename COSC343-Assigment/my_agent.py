__author__ = "Kris Mao"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "maokr879@student.otago.ac.nz"
__credit__ = "https://stackoverflow.com/questions/62430071/donald-knuth-algorithm-mastermind"
__credit__ = "https://www.tutorialspoint.com/symmetric-min-max-heaps"
__credit__ = "https://www.cs.uni.edu/~wallingf/teaching/cs3530/resources/knuth-mastermind.pdf"
import itertools
import random
import numpy as np
from mastermind import evaluate_guess

# Global variable
all_combinations = []


class MastermindAgent():
   """
             A class that encapsulates the code dictating the
             behaviour of the agent playing the game of Mastermind.

             ...

             Attributes
             ----------
             code_length: int
                 the length of the code to guess
             colours : list of char
                 a list of colours represented as characters
             num_guesses : int
                 the max. number of guesses per game

             Methods
             -------
             AgentFunction(percepts)
                 Returns the next guess of the colours on the board
             """

   def __init__(self, code_length,  colours, num_guesses):
      """
      :param code_length: the length of the code to guess
      :param colours: list of letter representing colours used to play
      :param num_guesses: the max. number of guesses per game
      """

      self.code_length = code_length
      self.colours = colours
      self.num_guesses = num_guesses
      self.all_combinations = []

      
   def random_pick(self, last_guess, all_combinations, place, color):
      # print(all_combinations)
      random_guess = random.choice(all_combinations)
      score = evaluate_guess(last_guess, random_guess) 
      if score[0] < place and score[1] < color:
         # print("yeas")
         all_combinations.remove(random_guess)
         self.random_pick(last_guess, all_combinations, place, color)  # Include all_combinations argument
      else:
         all_combinations.remove(random_guess)
         return np.array(random_guess)  # Move the return statement here



   def miniMax(self,possible_combinations):
      max_list = []#empty list for storing max score 
      for goal in possible_combinations: #searching each signal possible guess
         my_dict ={}#dict for store how many time each score appear
         for seeker in possible_combinations:#nest loop for every possible 
            if goal != seeker:# while goal and seeker are not same
               score = evaluate_guess(seeker,goal)# if the score are not show before we append it to dict
               if score not in my_dict:
                  my_dict[score] = 1
               else: #otherwise add one on time of appears
                  my_dict[score] += 1
         if my_dict:  # Check if my_dict is not empty before finding the maximum
            max_score_for_goal = max(my_dict.values(), default=0)  # Use default argument to handle empty dict
         else:
            max_score_for_goal = 0  # Set default value to 0 if the dict is empty
         max_list.append(max_score_for_goal)#append it  to max_list
      #For the return we need to pick the smallest one, coz we using minimax algorithm
      return possible_combinations[max_list.index(min(max_list))]
      
            

   def AgentFunction(self, percepts):
      """Returns the next board guess given state of the game in percepts

            :param percepts: a tuple of four items: guess_counter, last_guess, in_place, in_colour

                     , where

                     guess_counter - is an integer indicating how many guesses have been made, starting with 0 for
                                     initial guess;

                     last_guess - is a num_rows x num_cols structure with the copy of the previous guess

                     in_place - is the number of character in the last guess of correct colour and position

                     in_colour - is the number of characters in the last guess of correct colour but not in the
                                 correct position

            :return: list of chars - a list of code_length chars constituting the next guess
            """
 
     
      
      guess_counter, last_guess, in_place, in_colour = percepts
     

      if guess_counter == 0 :## frist guess pick PPPRR 
         actions = [self.colours[0]]*3 + [self.colours[1]]*2
         self.all_combinations = list(itertools.product(
             self.colours, repeat=self.code_length))
      elif guess_counter == 1: ## select a random one fomr possible combinations, evaluate it, if it's greater than current guess add in to vaild lists, otherwise do it again          
         self.all_combinations = [c for c in self.all_combinations if evaluate_guess(
              c, last_guess) == (in_place, in_colour)] #Reduce un-relate possible guess from original dataset
         self.all_combinations = [
             list(c) for c in self.all_combinations]  # make them to a list
         actions = self.random_pick(
             last_guess, self.all_combinations, in_place, in_colour)
         #randomly pick on possible guess and start form it.
      else:
         
         self.all_combinations = [c for c in self.all_combinations if evaluate_guess(
             c, last_guess) == (in_place, in_colour)]#again reduce un0relate possible guess from data set, imcrease the speed
         # make them  into a list
         self.all_combinations = [list(c) for c in self.all_combinations]
         # print("length:")
         # Testing, each time possbile combination shall reduce
         # print(len(self.all_combinations))
         # using minimax algrothm to solve this problem.
         actions = self.miniMax(self.all_combinations[:])
      
      #Return highest possible guess for next 
      return actions

