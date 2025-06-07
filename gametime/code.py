import stage
import ugame
import time
import random
import supervisor

import constants
import game_over

def sound_scene():
    """
    This function plays a sound when the game is booted up.
    """
    
    coin_sound = open("coin.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)
    sound.play(coin_sound)

    image_bank_mt_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    background = stage.Grid(image_bank_mt_background, constants.SCREEN_X, constants.SCREEN_Y)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [background]
    game.render_block()

    while True:
        time.sleep(1.0)
        menu_scene()

def menu_scene():
    """
    This function acts as the menu scene
    """
    
    # gets image bank
    image_bank_mt_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    text = []
    text1 = stage.Text(width=29, height=12, font=None, palette=constants.WHITE_PALETTE, buffer=None)
    text1.move(35,20)
    text1.text("World Cup")
    text.append(text1)

    text2 = stage.Text(width=29, height=12, font=None, palette=constants.WHITE_PALETTE, buffer=None)
    text2.move(35,110)
    text2.text("PRESS START")
    text.append(text2)

    background = stage.Grid(image_bank_mt_background, constants.SCREEN_X, constants.SCREEN_Y)

    # used this program to split the image into tile: 
    #   https://ezgif.com/sprite-cutter/ezgif-5-818cdbcc3f66.png
    background.tile(2, 2, 0)  # blank white
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)
    background.tile(7, 2, 0)  # blank white

    background.tile(2, 3, 0)  # blank white
    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)
    background.tile(7, 3, 0)  # blank white

    background.tile(2, 4, 0)  # blank white
    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)
    background.tile(7, 4, 0)  # blank white

    background.tile(2, 5, 0)  # blank white
    background.tile(3, 5, 0)
    background.tile(4, 5, 13)
    background.tile(5, 5, 14)
    background.tile(6, 5, 0)
    background.tile(7, 5, 0)  # blank white

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()
    
    # repeat forever..
    while True:
        keys = ugame.buttons.get_pressed()

        if keys & ugame.K_START != 0:
            tutorial()

        game.tick()

def tutorial():
    """
    This function acts as the menu scene
    """

    text = []
    text1 = stage.Text(width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None)
    text1.move(5,10)
    text1.text("Let's play football!")
    text.append(text1)

    text2 = []
    text2 = stage.Text(width=25, height=12, font=None, palette=constants.RED_PALETTE, buffer=None)
    text2.move(5,40)
    text2.text("Avoid the Happy Meals.")
    text.append(text2)

    text3 = stage.Text(width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None)
    text3.move(5,70)
    text3.text("Collect Dr Pepper. ")
    text.append(text3)

    text4 = stage.Text(width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None)
    text4.move(5,90)
    text4.text("Continue (Press B) ")
    text.append(text4)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text
    game.render_block()
    
    # repeat forever..
    while True:
        keys = ugame.buttons.get_pressed()

        if keys & ugame.K_O != 0:
            game_scene()

        game.tick()



def game_scene():
    """
    This function codes for the gaming parts
    """

    def show_card():
        # this function takes an card from off screen and moves it on screen
        for card_number in range(len(cards)):
            if cards[card_number].y < 0:
                cards[card_number].move(constants.OFF_TOP_SCREEN, random.randint(0 + constants.SPRITE_SIZE, constants.SCREEN_Y - constants.SPRITE_SIZE))
                break

    def show_goal():
        # this function takes a goal from off screen and moves it on screen
        for goal_number in range(len(goals)):
            if goals[goal_number].y < 0:
                goals[goal_number].move(random.randint(10, 140), random.randint(10, 108))
                break

    image_bank_background = stage.Bank.from_bmp16("space_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_sprites.bmp")

    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    goalt_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # for score
    card_count = 0

    kick_sound = open("kick.wav", "rb")
    cheer_sound = open("cheer.wav", "rb")
    booking_sound = open("booking.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    background = stage.Grid(image_bank_background, constants.SCREEN_X, constants.SCREEN_Y)

    kori = stage.Sprite(image_bank_sprites, 0, 60, 62)

    # keeps track of score
    score = 0
    score_text = stage.Text(width=29, height=14, font=None, palette=constants.RED_PALETTE, buffer=None)
    score_text.clear()
    score_text.cursor(0,0)
    score_text.move(1,1)
    score_text.text("Score: {0}".format(score))

    # makes background tiles randomized
    for x_location in range(constants.SCREEN_GRID_X):
        for y_location in range(constants.SCREEN_GRID_Y):
            tile_picked = random.randint(0, 1)
            background.tile(x_location, y_location, tile_picked)

    # create a list of balls for when we shoot
    balls = []
    for ball_number in range(constants.TOTAL_NUMBER_OF_BALLS):
        a_single_ball = stage.Sprite(image_bank_sprites, 2, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
        balls.append(a_single_ball)

    cards = []
    for card_number in range(constants.TOTAL_NUMBER_OF_CARDS):
        a_single_card = stage.Sprite(image_bank_sprites, 4, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
        cards.append(a_single_card)
    show_card()

    goals = []
    for goal_number in range(constants.TOTAL_NUMBER_OF_GOALS):
        a_single_goal = stage.Sprite(image_bank_sprites, 5, random.randint(10, 140), random.randint(10, 108))
        goals.append(a_single_goal)
    show_goal()

    # set the layers of all sprites, items show up in order
    # and set the frame rate to 60fps
    game = stage.Stage(ugame.display, 60)
    game.layers = [score_text] + goals + cards + balls + [kori] + [background]
    game.render_block()

    while True:
        keys = ugame.buttons.get_pressed()

        # kori movement code

        def ball_shoot():
            """
            This function controls the balls travelling to the right when a button is pressed.
            """

        ball_shoot()

        # move cards
        for card_number in range(len(cards)):
            if cards[card_number].y > 0:
                cards[card_number].move(cards[card_number].x + constants.ASTEROID_SPEED, cards[card_number].y)
                if cards[card_number].x > constants.SCREEN_X:
                    cards[card_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    show_card()

        # if a ball hits a goal, add one point to player's score
        for ball_number in range(len(balls)):
            if balls[ball_number].x > 0:
                for goal_number in range(len(goals)):
                    if goals[goal_number].x > 0:
                        if stage.collide(balls[ball_number].x + 6, balls[ball_number].y + 2, balls[ball_number].x + 11, balls[ball_number].y + 12, goals[goal_number].x + 1, goals[goal_number].y, goals[goal_number].x + 15, goals[goal_number].y + 15):
                            goals[goal_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                            balls[ball_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                            sound.stop()
                            sound.play(cheer_sound)
                            score += 1
                            score_text.clear()
                            score_text.cursor(0,0)
                            score_text.move(1,1)
                            score_text.text("Score: {0}".format(score))
                            show_card()
                            show_card()
                            show_goal()
                            card_count = card_count + 1

        # if a ball hits an card, ball does nothing and is destroyed
        for ball_number in range(len(balls)):
            if balls[ball_number].x > 0:
                for card_number in range(len(cards)):
                    if cards[card_number].x > 0:
                        if stage.collide(balls[ball_number].x + 6, balls[ball_number].y + 2, balls[ball_number].x + 11, balls[ball_number].y + 12, cards[card_number].x + 1, cards[card_number].y, cards[card_number].x + 15, cards[card_number].y + 15):
                            balls[ball_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)

        for card_number in range(len(cards)):
            if cards[card_number].x > 0:
                if stage.collide(cards[card_number].x + 1, cards[card_number].y, cards[card_number].x + 15, cards[card_number].y + 15, kori.x, kori.y, kori.x + 15, kori.y+15):
                    sound.stop()
                    sound.play(booking_sound)
                    time.sleep(3)
                    game_over.game_over_scene(score)

        game.render_sprites(goals + cards + balls + [kori])
        game.tick()


if __name__ == "__main__":
    sound_scene()
