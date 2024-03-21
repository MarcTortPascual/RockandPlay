import pygame as pg
import pygamepopup as pgp
from card import Card
from game import Game
import pygame_gui as gui
from screen import ScreenManager
from sound import SoundManager

pg.init()
pgp.init()

running = True

pg.display.set_caption("PyCard")
screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN | pg.SCALED)

clock = pg.time.Clock()

game: Game = None

with open("./house_rules", "rt") as f:
    house_rules_code = int(f.read())

ScreenManager.return_to_main_menu()
while running:

    dt = clock.tick(60) / 1000

    if ScreenManager.current_screen == 0:
        # Main menu
        screen.fill("black")
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == gui.UI_BUTTON_PRESSED:
                SoundManager.button()
                if event.ui_element == ScreenManager.play_button:
                    ScreenManager.current_screen = 1
                    game = Game(screen, 4, house_rules_code)
                if event.ui_element == ScreenManager.online_button:
                    ScreenManager.current_screen = 1
                    game = Game(screen, 2, house_rules_code)
                if event.ui_element == ScreenManager.quit_button:
                    running = False
            ScreenManager.main_manager.process_events(event)
        ScreenManager.main_manager.update(dt)
        ScreenManager.main_manager.draw_ui(screen)
        pg.display.update()

    if ScreenManager.current_screen == 1:
        if game:
            running = game.main_game_loop()
pg.quit()