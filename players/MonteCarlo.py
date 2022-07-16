"""
File: players/MonteCarlo.py
File Created: 16/07/2022
Authors: Louis Geisler, Emile Duquennoy
"""

from random import sample


class MonteCarlo:
    def __init__(self, Jeu):
        print("Initializing", self)
        self.n = int(input("How many tests? "))

    def Choix(self, Partie):
        def Test(coup):
            p = Partie.DeepCopy()
            Etat = p.Jouer(coup)
            if Etat[0]:
                return Etat[1]
            else:
                return self.Heuristique(p)

        l = [[coup, Test(coup)] for coup in Partie.lCoupJouable]
        print("Estimates", self, ":", l)
        return [min, max][Partie.joueur](l, key=lambda x: x[1])[0]

    def Heuristique(self, Partie):

        Resultat = 0
        for i in range(self.n):
            p = Partie.DeepCopy()
            Etat = (False, 0)
            while not Etat[0]:
                Etat = p.Jouer(sample(p.lCoupJouable, 1)[0])
            if Etat[1] == (-1, 1)[Partie.joueur]:  # Si
                Resultat += Etat[1]

        return Resultat / self.n

    def __repr__(self):
        return "MonteCarlo player"
