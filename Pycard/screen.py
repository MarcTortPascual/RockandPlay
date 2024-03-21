import pygame as pg
import pygame.freetype as freetype
import pygame_gui as gui

from sound import SoundManager
freetype.init()
class ScreenManager:
    current_screen = 0

    main_manager = gui.UIManager((1920, 1080))

    play_button = gui.elements.UIButton(
        relative_rect=pg.Rect(((1920 - 240) // 2, (1080 - 80) // 2 - 120), (240, 80)),
        text="Start Local Game",
        manager=main_manager
    )
    online_button = gui.elements.UIButton(
        relative_rect=pg.Rect(((1920 - 240) // 2, (1080 - 80) // 2), (240, 80)),
        text="Start Online Game",
        manager=main_manager
    )
    quit_button = gui.elements.UIButton(
        relative_rect=pg.Rect(((1920 - 240) // 2, (1080 - 80) // 2 + 120), (240, 80)),
        text="Exit to Desktop",
        manager=main_manager
    )
    
    # Online Mode stuff
    online_manager = gui.UIManager((1920, 1080))

    def return_to_main_menu():
        SoundManager.main_menu()
        ScreenManager.current_screen = 0