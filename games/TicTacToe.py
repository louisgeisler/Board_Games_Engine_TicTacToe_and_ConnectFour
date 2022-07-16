"""
File: games/TicTacToe.py
File Created: 16/07/2022
Authors: Louis Geisler, Emile Duquennoy
"""

from utils.Console import colorPrint

class TicTacToe:

    def __init__(self,plateau=[0]*9, nTour=0, lCoupJouable=list(range(9))):
        self.plateau=plateau
        self.nTour=nTour
        self.lCoupJouable=lCoupJouable

    @property
    def joueur(self):
        return self.nTour%2

    def DeepCopy(self):
        return TicTacToe(self.plateau.copy(), self.nTour, self.lCoupJouable.copy())

    def GetCase(self,coup):
        return self.plateau[coup]

    def Coup2Case(self, coup):
        return coup%3,coup//3

    def Coup2Affiche(self,coup):
        return self.Coup2Case(coup)

    def Gain(self,coup):
        """ Return (End? , Gain) """
        x,y=self.Coup2Case(coup)
        gain=sum(map(lambda l: int(sum(l)/3),  [self.plateau[x:9:3],
                                                self.plateau[y*3:y*3+3],
                                                self.plateau[2:7:2],
                                                self.plateau[0:9:4]]))
        if gain!=0:
            return (True, self.plateau[coup])
        else:
            return (self.lCoupJouable==[], 0)
        
    def Jouer(self,coup):
        self.lCoupJouable.remove(coup)
        self.plateau[coup]=(-1, 1)[self.joueur]
        self.nTour+=1
        return self.Gain(coup)

    def Affichage(self):
        a=self.plateau.copy()
        print(" "*2+" ".join(list(map(str,range(3)))))
        for i in range(3):
            print(str(i)+" ", end="")
            for v in a[:3]:
                colorPrint(*(("X","Green"), (".","Blue") ,("O","Red"))[v+1])
            print("")
            a=a[3:]
