"""
File: players/MinMax.py
File Created: 16/07/2022
Authors: Louis Geisler, Emile Duquennoy
"""

from players.MonteCarlo import MonteCarlo


class MinMax:
    def __init__(self, Jeu):
        print("Initializing MinMax")
        self.profondeurMax = int(
            input(
                "What depth of tree do you want to explore (-1 to explore all): "
            )
        )
        if self.profondeurMax >= 0:
            self.Heuristique = MonteCarlo(Jeu).Heuristique

    def Choix(self, Partie):
        def evaluation(Partie, coup, profondeur):
            Etat = Partie.Jouer(coup)
            if Etat[0]:
                return Etat[1]
            elif profondeur == self.profondeurMax:
                return self.Heuristique(Partie)
            else:
                return imisation(Partie, profondeur)[0]

        def imisation(Partie, profondeur=0):
            return [min, max][Partie.joueur](
                [
                    (evaluation(Partie.DeepCopy(), coup, profondeur + 1), coup)
                    for coup in Partie.lCoupJouable
                ],
                key=lambda x: x[0],
            )

        print("The computer is playing !!!")
        return imisation(Partie)[1]

    def __repr__(self):
        return "MinMax player"
