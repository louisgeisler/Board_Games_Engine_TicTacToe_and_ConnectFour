"""
File: main.py
File Created: 16/07/2022
Authors: Louis Geisler, Emile Duquennoy
"""

from textwrap import dedent

from utils.FilesUtils import get_list_imported_classes
import players
import games


PLAYERS = get_list_imported_classes(players)
GAMES = get_list_imported_classes(games)


def Partie(Partie,*lJoueur):

    lJoueur = lJoueur[0](Partie),lJoueur[1](Partie)
    print("-"*30)

    Etat=(False,0)
    while not Etat[0]:
        Partie.Affichage()

        available_moves = [Partie.Coup2Affiche(c) for c in Partie.lCoupJouable]

        print(dedent(f"""\
        
        Round N°{Partie.nTour}
        Current player: {lJoueur[Partie.nTour%2]}

        Players:
            X: {lJoueur[0]}
            O: {lJoueur[1]}
        
        Possible moves: {available_moves}
        """))

        coup=lJoueur[Partie.joueur].Choix(Partie)
        Etat=Partie.Jouer(coup)

        print(dedent(f"""\
             
        Last move: {Partie.Coup2Affiche(coup)}
        Eta: {Etat}
        """))
 

    Partie.Affichage()

    winner = (lJoueur[0], "Tie", lJoueur[1])[Etat[1]+1]
    print(dedent(f"""\

    Game Over !
    Score: {Etat[1]}
    Eta: {Etat}
    
    Winner: {winner}
    """))


if __name__ == "__main__":

    # Choice of game to play
    print("Games available:")
    for i,jeu in enumerate(GAMES):
        print(f"    {i})",jeu.__name__)
    Jeu=GAMES[int(input(f"Which game do you want to play? (number) "))]

    # The type of player for the game
    print("\nPlayers available:")
    for i,joueur in enumerate(PLAYERS):
        print(f"    {i})",joueur.__name__)
    lJ=[]
    for i in [1,2]:
        lJ+=[PLAYERS[int(input(f"Player{i}'s type: "))]]
    
    print("-"*30)
    
    Partie(Jeu(),*lJ)
