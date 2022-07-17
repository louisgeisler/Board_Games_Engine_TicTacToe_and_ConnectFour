import eel
import random
import os


eel.init(os.path.join(__file__, '..', 'web'))


eel.start('board.html', size=(400, 300))

callback = None

def wait_for_player_choice(callback):
    callback = callback
    

@eel.expose
def colomn_clicked(column):
    callback(column)

    

@eel.expose
def loaded():
    print("loaded")
    
@eel.expose
def add_pawn(column):
    eel.add_pawn(column)


