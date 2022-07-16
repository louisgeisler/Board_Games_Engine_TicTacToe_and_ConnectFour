"""
File: utils/Console.py
File Created: 16/07/2022
Authors: Louis Geisler, Emile Duquennoy
"""

import sys


# Definition de la fonction d'affichage des couleurs
try:
    sys.stdout.shell.write("")
    dColor = {"Blue": "DEFINITION", "Green": "STRING", "Red": "COMMENT"}

    def colorPrint(text, couleur):
        assert couleur in dColor
        sys.stdout.shell.write(text, dColor[couleur])


except AttributeError:
    dColor = {"Blue": "\033[1;34m", "Green": "\033[0;32m", "Red": "\033[1;31m"}

    def colorPrint(text, couleur):
        assert couleur in dColor
        print(dColor[couleur] + text + "\033[0;0m", end="")
