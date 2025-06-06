import stage
import supervisor
import ugame 
import random
import time

import constants

def game_over_scene(final_score):
    sound = ugame.audio
    sound.stop()

    image_bank_2 = stage.Bank.from_bmp16("mt_game_studio.bmp")

    background = stage.Grid(image_bank_2, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)

    text = []
    
    # ...existing code...
    text1.text("Final Score: {:0>2d}".format(final_score))
    text.append(text1)

    text2 = stage.Text(width=29, height =14, font=None, palette=constants.BLUE_PALETTE, buffer=None)
    text2.move(43,60)
    text2.text("MISSION FAILED")
    text.append(text2)

    text3 = stage.Text(width=29, height =14, font=None, palette=constants.BLUE_PALETTE, buffer=None)
    text3.move(32,110)
    text3.text("Play Again?")
    text.append(text3)
# ...existing code...

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()

    while True:
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_SELECT != 0:
            supervisor.reload()

        game.tick()