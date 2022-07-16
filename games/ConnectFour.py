"""
File: games/ConnectFour.py
File Created: 16/07/2022
Authors: Louis Geisler, Emile Duquennoy
"""

from utils.Console import colorPrint

class ConnectFour:

    def __init__(self,largeur=7,hauteur=6,plateau=None, nTour=0, lCoupJouable=None, dernierCoup=None):
        self.largeur=largeur
        self.hauteur=hauteur
        self.plateau=plateau
        self.nTour=nTour
        self.dernierCoup=dernierCoup
        self.lCoupJouable=lCoupJouable
        
        if self.plateau is None:
            self.plateau=np.zeros((self.largeur,self.hauteur), dtype=int)
        if self.lCoupJouable is None:
            self.lCoupJouable=[(x,0) for x in range(self.largeur)]

    def DeepCopy(self):
        return ConnectFour(self.largeur,  self.hauteur, self.plateau.copy(), self.nTour, self.lCoupJouable.copy(), self.dernierCoup)
    
    @property
    def joueur(self):
        return self.nTour%2

    def GetCase(self,coup):
        return self.plateau[coup]

    def Coup2Etat(self,coup):
        return self.GetCase(coup)+2*(coup in self.lCoupJouable)

    def Coup2Case(self, coup):
        return coup

    def Case2Coup(self,x,y):
        return (x,y)

    def Coup2Affiche(self,coup):
        return coup[0]
        
    def Gain(self,coup):
        #Renvoie (Fin? , Gain)
        x,y=self.Coup2Case(coup)
        vJ=(-1,1)[self.joueur]
        
        for vx,vy in [[1,0], [0,1], [1,1], [1,-1]]:
            pionAligne=1
            for vx,vy in [[vx,vy],[-vx,-vy]]:
                for i in range(1,4):
                    xi, yi=x+i*vx, y+i*vy
                    if (0<=xi<self.largeur and 0<=yi<self.hauteur and self.plateau[xi,yi]==vJ):
                        pionAligne+=1
                    else:
                        break
            
            if pionAligne>=4:
                return (True, vJ)
        
        return (self.lCoupJouable==[], 0)
    
    def Jouer(self,coup):
        assert coup in self.lCoupJouable
        x,y=self.Coup2Case(coup)
        self.lCoupJouable.remove(coup)
        if y+1<self.hauteur:
            self.lCoupJouable+=[(x,y+1)]
        self.dernierCoup=(x,y)
        self.plateau[x,y]=(-1,1)[self.joueur]
        Etat=self.Gain(coup)
        self.nTour+=1
        return Etat

    def Affichage(self):
        for y in range(self.hauteur):
            for x in range(self.largeur):
                colorPrint(*(("X","Green"), (".","Blue") ,("O","Red"))[self.plateau[x, self.hauteur-1-y]+1])
            print("")
        colorPrint("".join(map(str,range(self.largeur)))+"\n", "Blue")
