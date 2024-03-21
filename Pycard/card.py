import os.path
import pygame as pg

class Card:
    def __init__(self, _game, _screen: pg.Surface, _color: str, _type: str, _size: pg.Vector2) -> None:
        self.color = _color
        self.game = _game
        self.type = _type
        self.screen = _screen
        self.w = _size.x
        self.h = _size.y
        self.rect: pg.Rect
        self.card_image = pg.transform.scale(pg.image.load(os.path.join("assets", "cards", f"{self.color[0].upper() if len(self.color) > 0 else ""}{self.type}.jpg")), _size)

    def is_playable(self, target) -> bool:
        
        if self.color == target.color or self.type == target.type or self.color == "":
            return True

        if not target:
            return True

        return False

    def is_identical(self, target) -> bool:

        if self.color == target.color and self.type == target.type:
            return True
        
        if not target:
            return True
        
        return False

    def update_front(self):
        self.card_image = pg.transform.scale(pg.image.load(os.path.join("assets", "cards", f"{self.color[0].upper() if len(self.color) > 0 else ""}{self.type}.jpg")), (self.w, self.h))

    def show_card(self, pos: pg.Vector2, vertical: bool = False, enabled: bool = True):
        pos = pg.Vector2(pos.x - self.w / 2, pos.y - self.h / 2)
        size = pg.Vector2(self.w, self.h)
        # pg.draw.rect(self.screen, self.color, rect)
        self.rect = pg.Rect(pos.x, pos.y, size.x, size.y)
        card_copy = pg.transform.rotate(self.card_image.copy(), 90 if vertical else 0).convert_alpha()
        self.screen.blit(card_copy, pos)
        if not enabled:
            card_copy.fill(pg.Color(0, 0, 0, 128))
            self.screen.blit(card_copy, pos)
    
    def hide_card(self, pos: pg.Vector2, vertical: bool = False):
        pos = pg.Vector2(pos.x - self.w / 2, pos.y - self.h / 2)
        size = pg.Vector2(self.w, self.h)
        # pg.draw.rect(self.screen, self.color, rect)
        self.rect = pg.Rect(pos.x, pos.y, size.x, size.y)
        self.screen.blit(pg.transform.rotate(self.game.card_back, 90 if vertical else 0), pos)