"""
File: players/Random.py
File Created: 16/07/2022
Authors: Louis Geisler, Emile Duquennoy
"""

from random import sample


class Random:
    def __init__(self, Jeu):
        print("Initializing", self)

    def Choix(self, Partie):
        # return sorted(Jeu.lCoupJouable, key=lambda x: x[0])[0]
        return sample(Partie.lCoupJouable, 1)[0]

    def __repr__(self):
        return "Random choice player"
