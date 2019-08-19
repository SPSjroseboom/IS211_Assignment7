#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""assignment7 - game.py
Created on Sun Aug 18 21:30:23 2019
@author: SPSjonathan
"""


import random
import re


class User(object):

    def __init__(self):
        self.name = raw_input('Enter a player name: ').strip()
        self.player_score = 0

    def add_points(self, points):
        self.player_score += points


class Die(object):

    # Choose how many sides your die has
    def __init__(self, sides):
        self.sides = [i + 1 for i in range(sides)]

    def roll(self):
        return random.choice(self.sides)


class PigGameInstance(object):

    def __init__(self):
        self.player_data = {}
        self.pending_points = 0
        self.current_player_turn = None

    def add_player(self, user):
        self.player_data[user.name] = user.player_score

    def check_if_winner(self):
        for key, val in self.player_data.items():
            if val >= 100:
                print '{} has won the game! \nType r or h to play again!\n'.format(
                    key)
                self.reset_state()
                quit()

    def display_scores(self):
        # Format the dictionary entries and join the list to the string
        print '''\n***** SCOREBOARD *****\n\n{}\n\n**********************\n
        '''.format(' \n'.join('{} : {}'.format(key, val) for (key, val) in self.player_data.items()))

    def reset_state(self):
        self.player_data.clear()
        self.pending_points = 0

    def get_current_player(self):
        return self.current_player_turn

    def player_turn(self):
        # Get input and validate
        while True:
            player_response = raw_input(
                'Will you Roll or Hold? (r for Roll, h for Hold)\n').strip()
            if not re.match(r'(r|h)', player_response, flags=re.IGNORECASE):
              print 'Please enter a valid move.'
              continue
            else:
              return player_response
              break


def main():

    # Initialize game
    pig_game = PigGameInstance()
    game_die = Die(6)

    # Set up the match
    player_count = int(
        raw_input('How many players?: ').strip())
    for _ in range(player_count):
        pig_game.add_player(User())

    # There needs to be at least 2 players

    print '\n***** Welcome to the game of PIG! *****\n'
    print '''
    Rules: Each turn, a player repeatedly rolls a 6-sided die.
    Every time you roll a 2, 3, 4, 5 or 6- it gets added to your total
    and you can choose to keep going or hold your winnings and pass your turn.
    If you roll a 1- you don't score any points and you pass your turn.
    The first person to get to 100 points wins!
    '''.center(6)

    while pig_game:

        for key, val in pig_game.player_data.items():
            pig_game.current_player_turn = key
            curr_player = pig_game.get_current_player()
            bad_roll = False

            # If the roll is bad then the next player will have their turn
            while bad_roll == False:
                print '\nIt\'s {}\'s turn: '.format(key)
                response = pig_game.player_turn()
                print '\n'
                if re.match(r'(roll|r)', response, flags=re.IGNORECASE):
                    current_roll = game_die.roll()
                    if current_roll == 1:
                        print '{} rolled a 1: You lost it all! \n'.format(key)
                        bad_roll = True
                        pig_game.pending_points = 0
                        break
                    else:
                        print '\n{} rolled a: {}'.format(key, current_roll)
                        pig_game.pending_points += current_roll
                        pig_game.display_scores()
                        print 'Pending points: {} \n'.format(
                            pig_game.pending_points)
                        pig_game.check_if_winner()
                else:
                    pig_game.player_data[curr_player] += pig_game.pending_points
                    pig_game.pending_points = 0
                    break


if __name__ == '__main__':
    main()