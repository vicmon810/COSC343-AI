
import itertools
import numpy as np
from mastermind import max_possible_guess,\
    min_possible_guess,\
    evaluate_guess,\
    possible_guess
class MastermindAgent():
    """
    A class that encapsulates the code dictating the
    behavior of the agent playing the game of Mastermind.
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

    def __init__(self, code_length, colours, num_guesses):
        """
        :param code_length: the length of the code to guess
        :param colours: list of letter representing colours used to play
        :param num_guesses: the max. number of guesses per game
        """

        self.code_length = code_length
        self.colours = colours
        self.num_guesses = num_guesses

    def minimax_score(self, guess, possible_codes, remaining_guesses, maximizing_player):
        if remaining_guesses == 0:
            return 0

        if maximizing_player:  # The guesser tries to maximize the score
            best_score = float('-inf')
            for code in possible_codes:
                in_place, in_colour = evaluate_guess(guess, code)
                score = in_place + in_colour + \
                    self.minimax_score(guess, possible_codes,
                                       remaining_guesses - 1, False)
                best_score = max(best_score, score)
            return best_score

        else:  # The opponent (code maker) tries to minimize the score
            best_score = float('inf')
            for code in possible_codes:
                in_place, in_colour = evaluate_guess(guess, code)
                score = -(in_place + in_colour) + self.minimax_score(guess,
                                                                     possible_codes, remaining_guesses - 1, True)
                best_score = min(best_score, score)
            return best_score

    def minimax_guess(self, possible_codes, remaining_guesses):
        best_guess = None
        best_score = float('-inf')

        for code in possible_codes:
            score = self.minimax_score(
                code, possible_codes, remaining_guesses - 1, True)
            if score > best_score:
                best_score = score
                best_guess = code

        return best_guess

    def AgentFunction(self, percepts):
        """
        Returns the next board guess given the state of the game in percepts

        :param percepts: a tuple of four items: guess_counter, last_guess, in_place, in_colour

                , where

                guess_counter - is an integer indicating how many guesses have been made, starting with 0 for
                                the initial guess;

                last_guess - is a num_rows x num_cols structure with the copy of the previous guess

                in_place - is the number of characters in the last guess of correct colour and position

                in_colour - is the number of characters in the last guess of correct colour but not in the
                            correct position

        :return: list of chars - a list of code_length chars constituting the next guess
        """
        # Extract different parts of percepts.
        guess_counter, last_guess, in_place, in_colour = percepts

        if guess_counter == 0:
            # Make an initial guess with fixed colours to reduce redundancy and improve performance.
            initial_guess = [self.colours[0]] * self.code_length
            return initial_guess

        # Generate all possible codes based on the available colours and code length
        possible_codes = np.array(
            list(itertools.product(self.colours, repeat=self.code_length)))

        # Use the Minimax algorithm to make the next guess
        guess = self.minimax_guess(
            possible_codes, self.num_guesses - guess_counter)

        return guess
