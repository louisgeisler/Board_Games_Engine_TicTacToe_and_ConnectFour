"""
File: players/Human.py
File Created: 16/07/2022
Authors: Louis Geisler, Emile Duquennoy
"""

class Human:

    def __init__(self, Jeu):
        print("Initializing",self)

    def Choix(self, Jeu):
        for i,coup in enumerate(Jeu.lCoupJouable):
            print(f"    {i})", Jeu.Coup2Affiche(coup))
        return Jeu.lCoupJouable[int(input("\nYour choice's number: "))%len(Jeu.lCoupJouable)]

    def __repr__(self):
        return "Human player"

