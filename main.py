from random import *
from itertools import *
import numpy as np
import sys


##########################################################
#                                                        #
#     Premature Optimization Is the Root of All Evil     #
#                                                        #
##########################################################

# Definition de la fonction d'affichage des couleurs
try:
    sys.stdout.shell.write("")
    dColor={"Bleu": "DEFINITION", "Vert": "STRING", "Rouge": "COMMENT"}
    def colorPrint(text, couleur):
        assert couleur in dColor
        sys.stdout.shell.write(text, dColor[couleur])
except AttributeError:
    dColor={"Bleu": "\033[1;34m", "Vert": "\033[0;32m", "Rouge": "\033[1;31m"}
    def colorPrint(text, couleur):
        assert couleur in dColor
        print(dColor[couleur]+text+'\033[0;0m', end="")


####### Joueurs #######

class Humain:

    def __init__(self, Jeu):
        print("Initialisation",self)

    def Choix(self, Jeu):
        for i,coup in enumerate(Jeu.lCoupJouable):
            print(str(i)+")",Jeu.Coup2Affiche(coup))
        return Jeu.lCoupJouable[int(input("\nNuméro de votre choix: "))%len(Jeu.lCoupJouable)]

    def __repr__(self):
        return "Joueur Humain"


class Alea:

    def __init__(self, Jeu):
        print("Initialisation", self)

    def Choix(self, Partie):
        #return sorted(Jeu.lCoupJouable, key=lambda x: x[0])[0]
        return sample(Partie.lCoupJouable,1)[0]

    def __repr__(self):
        return "Joueur Aléatoire"


class MonteCarlo:

    def __init__(self, Jeu):
        print("Initialisation",self)
        self.n=int(input("Combien de test ? "))

    def Choix(self, Partie):
        
        def Test(coup):
            p=Partie.DeepCopy()
            Etat=p.Jouer(coup)
            if Etat[0]:
                return Etat[1]
            else:
                return self.Heuristique(p)
        
        l=[[coup, Test(coup)] for coup in Partie.lCoupJouable]
        print("Estimations",self,":",l)
        return [min,max][Partie.joueur](l, key=lambda x: x[1])[0]
        

    def Heuristique(self, Partie):
        
        Resultat=0
        for i in range(self.n):
            p=Partie.DeepCopy()
            Etat=(False, 0)
            while not Etat[0]:
                Etat=p.Jouer(sample(p.lCoupJouable,1)[0])
            if Etat[1]==(-1, 1)[Partie.joueur]: # Si 
                Resultat+=Etat[1]
        
        return Resultat/self.n

    def __repr__(self):
        return "Joueur MonteCarlo"


class MinMax:

    def __init__(self, Jeu):
        print("Initialisation MinMax")
        self.profondeurMax=int(input("Quel profondeur d'arbre voulez-vous explorer ? (-1 pour tout explorer): "))
        if self.profondeurMax>=0:
            self.Heuristique=MonteCarlo(Jeu).Heuristique

    def Choix(self, Partie):
        
        def evaluation(Partie, coup, profondeur):
            Etat=Partie.Jouer(coup)
            if Etat[0]:
                return Etat[1]
            elif profondeur==self.profondeurMax:
                return self.Heuristique(Partie)
            else:
                return imisation(Partie,profondeur)[0]
                    
        def imisation(Partie, profondeur=0):
            return [min,max][Partie.joueur]([(evaluation(Partie.DeepCopy(), coup, profondeur+1), coup) for coup in Partie.lCoupJouable], key=lambda x: x[0])
        
        
        print("L'ordinateur joue !!!")
        return imisation(Partie)[1]

    def __repr__(self):
        return "Joueur MinMax"
    

####### JEUX #######

class Puissance4:

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
        return Puissance4(self.largeur,  self.hauteur, self.plateau.copy(), self.nTour, self.lCoupJouable.copy(), self.dernierCoup)
    
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
                colorPrint(*(("X","Vert"), (".","Bleu") ,("O","Rouge"))[self.plateau[x, self.hauteur-1-y]+1])
            print("")
        colorPrint("".join(map(str,range(self.largeur)))+"\n", "Bleu")


class Morpion:

    def __init__(self,plateau=[0]*9, nTour=0, lCoupJouable=list(range(9))):
        self.plateau=plateau
        self.nTour=nTour
        self.lCoupJouable=lCoupJouable

    @property
    def joueur(self):
        return self.nTour%2

    def DeepCopy(self):
        return Morpion(self.plateau.copy(), self.nTour, self.lCoupJouable.copy())

    def GetCase(self,coup):
        return self.plateau[coup]

    def Coup2Case(self, coup):
        return coup%3,coup//3

    def Coup2Affiche(self,coup):
        return self.Coup2Case(coup)

    def Gain(self,coup):
        """ Renvoie (Fin? , Gain) """
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
                colorPrint(*(("X","Vert"), (".","Bleu") ,("O","Rouge"))[v+1])
            print("")
            a=a[3:]

def Partie(Partie,*lJoueur):

    lJoueur=lJoueur[0](Partie),lJoueur[1](Partie)
    Etat=(False,0)
    while not Etat[0]:
        Partie.Affichage()
        print("Tour n°"+str(Partie.nTour)+"\nAu Joueur de jouer:", lJoueur[Partie.nTour%2],"\nEtat:",Etat)
        print("\nCoups Possibles: ", [Partie.Coup2Affiche(c) for c in Partie.lCoupJouable])
        #MonHeuristique(Partie)
        print(lJoueur)
        coup=lJoueur[Partie.joueur].Choix(Partie)
        print("\nCoup Choisi: ",Partie.Coup2Affiche(coup))
        Etat=Partie.Jouer(coup)
        #input("Appuyez sur une touche pour continuer !!!")

    Partie.Affichage()
    print("Fin ! \nScore:",Etat[1],"\nEtat:",Etat,"\nVainqueur:",(lJoueur[0],"Personne",lJoueur[1])[Etat[1]+1])

lJeu=(Morpion, Puissance4)
lJoueur=(Humain, Alea, MinMax, MonteCarlo)

#Partie(Morpion(),Alea,Alea)

# Choix du jeu
for i,jeu in enumerate(lJeu):
    print(str(i)+")",jeu.__name__)
Jeu=lJeu[int(input("Choix du Jeu "+str(i)+" : "))]
print("\n")

# Choix des joueurs
for i,joueur in enumerate(lJoueur):
    print(str(i)+")",joueur.__name__)
lJ=[]
for i in [1,2]:
    lJ+=[lJoueur[int(input("Choix du Joueur "+str(i)+" : "))]]

Partie(Jeu(),*lJ)
