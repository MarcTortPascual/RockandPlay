import random
from typing import Tuple
import pygame as pg
from card import Card
from sound import SoundManager
from rules import Rules

class Player:
    def __init__(self, game, index: int, pos: pg.Vector2, is_human: bool = False, vertical: bool = False) -> None:
        self.cards: list[Card] = []
        self.position = pos
        self.is_human = is_human
        self.game = game
        self.vertical = vertical
        self.index = index
        self.is_showing_hand = False
        self.has_said_uno = False
        self.can_be_challenged = False
        self.is_playing = False
        self.has_intercepted = False

    def show_hand(self, max: int, is_mine: bool = False, vertical: bool = False, active: bool = False):
        i = 0
        l = len(self.cards)
        if active:
            if vertical:
                hand_rect = pg.Rect(self.position.x - 65, self.position.y - 130 * (max / 2), 180, 120 * max)
            else:
                hand_rect = pg.Rect(self.position.x - 120 * (max / 2), self.position.y - 90, 120 * max, 180)
            pg.draw.rect(self.game.screen, "greenyellow", hand_rect)
        for c in self.cards:
            card_position: pg.Vector2
            new_pos: float
            if l > max:
                new_pos = c.w * (max / (l - 1)) * (i - (l - 1) / 2)
            else:
                new_pos = c.w * (i - (l - 1) / 2)
            if vertical:
                card_position = self.position + pg.Vector2(0, new_pos)
            else:
                card_position = self.position + pg.Vector2(new_pos, 0)
            if is_mine:
                top_discard_pile_card: Card = self.game.discard_pile[-1] if len(self.game.discard_pile) > 0 else None
                c.show_card(
                    card_position,
                    vertical,
                    self.is_human
                    and self.game.get_active_player() == self
                    and c.is_playable(top_discard_pile_card) or (self.game.draw_stack != 0 and c.type == "D2") or (self.game.house_rules & Rules.INTERCEPT != 0 and c == self.get_identical_card())
                )
            else:
                c.hide_card(card_position, vertical)
            i += 1

    
    def select_card(self, at: Tuple[int, int]) -> Card:
        # print(f"{at[0]}, {at[1]}")
        
        for card in self.cards[::-1]:
            if card.rect.collidepoint(at):
                return card
        
        return None

    def say_uno(self):
        if len(self.cards) == 2 and self.can_play() and not self.has_said_uno:
            if self.is_human:
                self.has_said_uno = True
            else:
                self.has_said_uno = True if random.random() < 0.75 else False

            if self.has_said_uno:
                SoundManager.yell_uno()
            

    def play_card(self, card: Card, time: int = 0):
        
        self.say_uno()

        self.cards.remove(card)
        last = now = pg.time.get_ticks()
        start_pos = self.position
        target_pos = pg.Vector2(self.game.screen.get_width() / 2, self.game.screen.get_height() / 2)

        SoundManager.play()

        self.is_playing = True

        while now - last < time:
            now = pg.time.get_ticks()
            self.game.render_game()
            card.show_card(pg.Vector2.lerp(start_pos, target_pos, min((now - last) / time, 1)))
            pg.display.flip()
            
        self.game.discard_pile.append(card)
        
        if not self.has_said_uno and len(self.cards) == 1:
            if self.is_human:
                pass
            else:
                self.game.wait(2000)

        if card.type == "SK":
            SoundManager.skip()
            self.game.skip_turn()
        if card.type == "RV":
            SoundManager.reverse()
            self.game.reverse_turn_order()
            
        intercepter: Player = self.game.get_player_with_identical_card()
        if intercepter and self.game.house_rules & Rules.INTERCEPT != 0:
            if intercepter.is_human:
                self.game.wait(2000)
                if intercepter.has_intercepted:
                    return

        if card.type == "D2":
            self.game.stack_plus_two()
            self.is_playing = False
            return
        if card.type == "WILD":
            if len(self.cards) > 0:
                if self.is_human:
                        self.game.popup_color_picker()
                else:
                    # print(self.get_mode_color())
                    self.game.change_top_card_color(self.get_mode_color())
            return
        if card.type == "WD4":
            if len(self.cards) > 0:
                if self.is_human:
                        self.game.popup_color_picker(True)
                else:
                    # print(self.get_mode_color())
                    self.game.change_top_card_color(self.get_mode_color(), True)
            return
        self.is_playing = False
        self.game.next_turn()
    
    def get_mode_color(self) -> int:
        modes: list[int] = []
        for c in self.game.colors:
            modes.append(len([i for i in self.cards if i.color == c]))
        
        return modes.index(max(modes))
    
    def has_color(self, color: str) -> bool:
        for card in self.cards:
            if card.color == color:
                return True
            
        return False
    
    def get_first_card_of_type(self, type: str) -> Card | None:
        return next((x for x in self.cards if x.type == type), None)
    
    def can_play(self) -> bool:
        for c in self.cards:
            if c.is_playable(self.game.discard_pile[-1]):
                return True
            
        return False
    
    def get_identical_card(self) -> Card | None:
        for c in self.cards:
            if c.type == self.game.discard_pile[-1].type and c.color == self.game.discard_pile[-1].color:
                return c
        return None