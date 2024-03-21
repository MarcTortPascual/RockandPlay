import sys
import pygame as pg
from pygamepopup.menu_manager import MenuManager
from pygamepopup.components import Button, InfoBox, TextElement
from card import Card
from player import Player
import random
import os.path
from sound import SoundManager
from rules import Rules
from screen import ScreenManager

class Game:
    def __init__(self, _screen: pg.Surface, _max_players: int, _rule_flags: int = 0, _online: bool = False):
        self.max_players = _max_players
        self.players: list[Player] = []
        self.screen = _screen
        self.colors = ["red", "green", "blue", "yellow"]
        self.actions = ["D2", "RV", "SK"]
        self.wildcards = ["WILD", "WD4"]
        self.clockwise = True
        self.house_rules = _rule_flags
        self.draw_stack = 0
        self.current_player_turn = 0
        self.game_flow_rotation = 0
        self.card_back = pg.transform.scale(pg.image.load(os.path.join("assets", "cards", "back.jpg")), (100, 150))

        self.uno_button = pg.transform.scale(pg.image.load(os.path.join("assets", "UNO_Logo.png")), (1280 // 5, 898 // 5))
        self.uno_button_rect = pg.Rect(0, 0, 0, 0)
        self.uno_button_pressed = False

        self.draw_key_pressed = False
        self.uno_key_pressed = False

        self.online = _online
        self.menu_manager = MenuManager(_screen)
        self.deciding = False

        self.deck: list[Card] = []
        self.deck_rect: pg.Rect
        self.deck_pressed = False

        self.generate_deck()
        self.discard_pile: list[Card] = []

        for i in range(_max_players):
            pos: pg.Vector2
            if i == 0:
                pos = pg.Vector2(self.screen.get_width() / 2, self.screen.get_height() - 150)
            elif i == 1:
                if _max_players > 2:
                    pos = pg.Vector2(150, self.screen.get_height() / 2)
                else:
                    pos = pg.Vector2(self.screen.get_width() / 2, 150)
            elif i == 2:
                if _max_players == 4:
                    pos = pg.Vector2(self.screen.get_width() / 2, 150)
                else:
                    pos = pg.Vector2(self.screen.get_width() - 150, self.screen.get_height() / 2)
            elif i == 3:
                pos = pg.Vector2(self.screen.get_width() - 150, self.screen.get_height() / 2)
            new_player = Player(self, i, pos, i == 0)
            self.deal_card(new_player, 7, 0)
            self.players.append(new_player)

        first_card = self.deck.pop()
        
        while first_card.type == "WD4":
            self.discard_pile.insert(0, first_card)
            first_card = self.deck.pop()

        self.discard_pile.append(first_card)

        SoundManager.game_bgm(1)

        if first_card.type == "SK":
            SoundManager.skip()
            self.next_turn()
        if first_card.type == "RV":
            SoundManager.reverse()
            self.reverse_turn_order()
        if first_card.type == "D2":
            self.stack_plus_two()
        if first_card.type == "WILD":
            if self.get_active_player().is_human:
                    self.popup_color_picker()
            else:
                # print(self.get_mode_color())
                self.change_top_card_color(self.get_mode_color())



    def motion(self, position: pg.Vector2):
        self.menu_manager.motion(position)

    def click(self, button: int, position: pg.Vector2):
        self.menu_manager.click(button, position)

    def main_game_loop(self) -> bool:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.MOUSEMOTION:
                self.motion(event.pos)
            if event.type == pg.MOUSEBUTTONDOWN:
                # selected_card = self.players[0].select_card(event.pos)
                self.uno_button_pressed = self.uno_button_rect.collidepoint(event.pos)
                self.deck_pressed = self.deck_rect.collidepoint(event.pos)
                intercepter = self.get_player_with_identical_card()
                if self.get_active_player().is_human and not self.deciding:
                    selected_card = self.get_active_player().select_card(event.pos)
                    if selected_card:
                        if selected_card.is_playable(self.discard_pile[-1]):
                            if self.draw_stack != 0:
                            # self.players[0].cards.remove(selected_card)
                                if selected_card.type == "D2":
                                    self.get_active_player().play_card(selected_card, 400)
                            else:
                                self.get_active_player().play_card(selected_card, 400)
                        else:
                            SoundManager.illegal_move()
                    if self.uno_button_pressed:
                        self.get_active_player().say_uno()
                        self.uno_button_pressed = False
                    if self.deck_pressed:
                        self.draw_card()
                        self.deck_pressed = False
                elif intercepter:
                    if intercepter.is_human and self.house_rules & Rules.INTERCEPT != 0:
                        selected_card = self.get_player_with_identical_card().select_card(event.pos)
                        if selected_card:
                            if selected_card.is_identical(self.discard_pile[-1]):
                                if selected_card.type == "D2":
                                    self.draw_stack = 0
                                self.current_player_turn = self.get_player_with_identical_card().index
                                self.get_player_with_identical_card().has_intercepted = True
                                self.get_player_with_identical_card().play_card(selected_card, 300)
                else:
                    if self.uno_button_pressed:
                        self.uno_challenge(self.get_active_player())
                        self.uno_button_pressed = False
                    
                    
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.click(event.button, event.pos)

            ScreenManager.main_manager.process_events(event)

        keys = pg.key.get_pressed()
        """
        if keys[pg.K_d]: # Draw
            if not self.draw_key_pressed:
                self.draw_key_pressed = True
                self.draw_card()
        else:
            self.draw_key_pressed = False
        """

        if keys[pg.K_u]: # UNO (Challenge)
            if not self.uno_key_pressed and not self.uno_button_pressed:
                self.uno_key_pressed = True
                current_player = self.get_active_player()
                if current_player.is_human:
                    current_player.say_uno()
                else:
                    if not current_player.has_said_uno and len(current_player.cards) == 1:
                        self.uno_challenge(current_player)
        else:
            self.uno_key_pressed = False  

        self.render_game()

        # flip() the display to put your work on screen
        pg.display.flip()

        return True

    def draw_card(self):
        if self.get_active_player().is_human:
            if self.draw_stack > 0:
                self.deal_card(self.get_active_player(), self.draw_stack)
                self.draw_stack = 0
            else:
                self.deal_card(self.get_active_player(), 1)
                if not self.get_active_player().cards[-1].is_playable(self.discard_pile[-1]):
                    self.next_turn()

    def render_game(self):
        self.screen.fill("darkgreen")

        for p in self.players:
            if self.max_players == 4:
                p.show_hand(8, (p.is_human or self.has_ended() or p.is_showing_hand) and not self.online, vertical=p.index % 2 != 0, active=p == self.get_active_player())
            else:
                p.show_hand(8, (p.is_human or self.has_ended() or p.is_showing_hand) and not self.online, False, p == self.get_active_player())
        self.show_discard_pile()
        self.show_deck()
        self.show_game_flow()
        self.show_uno_button()
        self.menu_manager.display()

    def wait(self, milis: int = 0):
        now = last = pg.time.get_ticks()
        while now - last < milis or (milis == 0 and self.deciding):
            now = pg.time.get_ticks()
            self.main_game_loop()

    def generate_random_card(self) -> Card:
        return Card(self.screen, random.choice(self.colors), str(random.randint(0, 9)), pg.Vector2(100, 150))

    def generate_deck(self):
        for c in self.colors:
            new_card = Card(self, self.screen, c, "0", pg.Vector2(100, 150))
            self.deck.append(new_card)
            for _ in range(2):
                for n in range(1, 10):
                    new_card = Card(self, self.screen, c, str(n), pg.Vector2(100, 150))
                    self.deck.append(new_card)
                for a in self.actions:
                    new_card = Card(self, self.screen, c, a, pg.Vector2(100, 150))
                    self.deck.append(new_card)
        for _ in range(4):
            for wc in self.wildcards:
                new_card = Card(self, self.screen, "", wc, pg.Vector2(100, 150))
                self.deck.append(new_card)
        random.shuffle(self.deck)
    
    def reset_deck(self):
        self.deck = self.discard_pile[:-2]
        self.discard_pile = self.discard_pile[-1:]

    def get_active_player(self) -> Player:
        return self.players[self.current_player_turn]

    def get_previous_player(self) -> Player:
        if self.clockwise:
            if self.current_player_turn == 0:
                return self.players[self.max_players - 1]
            return self.players[self.current_player_turn - 1]
        return self.players[(self.current_player_turn + 1) % self.max_players]

    def deal_card(self, player: Player, amount: int = 1, wait: int = 250):

        for _ in range(amount):
            # new_card = self.generate_random_card()
            cards_left = len(self.deck)
            # print(cards_left)
            if cards_left == 0:
                self.reset_deck()
            new_card = self.deck.pop()
            start_pos = pg.Vector2(
                (self.screen.get_width() - self.card_back.get_width()) * 0.75,
                (self.screen.get_height() - self.card_back.get_height()) * 0.5,
            )
            target_pos = player.position

            if wait > 0:
                SoundManager.draw()

            now = last = pg.time.get_ticks()
            
            while now - last < wait:
                now = pg.time.get_ticks()
                self.render_game()
                current_position = pg.Vector2.lerp(start_pos, target_pos, min((now - last) / wait, 1))
                if player.is_human:
                    new_card.show_card(current_position)
                else:
                    new_card.hide_card(current_position)
                pg.display.flip()
            player.cards.append(new_card)
        if wait > 0:
            self.wait(500)
        player.has_said_uno = False

        # print(len(self.deck))
    
    def show_discard_pile(self):
        for card in self.discard_pile:
            card.show_card(pg.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2))
    
    def show_game_flow(self):

        gf = pg.transform.rotate(pg.image.load(os.path.join("assets", "game_flow.png")), 45)

        if not self.clockwise:
            gf = pg.transform.flip(gf, True, False)

        self.screen.blit(gf, ((self.screen.get_width() - gf.get_width()) / 2, (self.screen.get_height() - gf.get_height()) / 2))

    def show_uno_button(self):
        current_player = self.get_active_player()
        if (not current_player.has_said_uno and not self.uno_button_pressed and
            ((current_player.is_human and len(current_player.cards) == 2 and current_player.can_play()) or
            len(current_player.cards) == 1)):
            self.uno_button_rect = self.screen.blit(
                self.uno_button,
                ((self.screen.get_width() - self.uno_button.get_width()) * 0.875, 
                (self.screen.get_height() - self.uno_button.get_height()) * 0.95)
            )
    
    def show_deck(self):
        self.deck_rect = self.screen.blit(
            self.card_back,
            (
                (self.screen.get_width() - self.card_back.get_width()) * 0.75,
                (self.screen.get_height() - self.card_back.get_height()) * 0.5,
            )
        )
        
    def get_hand_value(self, player: Player) -> int:
        score = 0
        for card in player.cards:
            if card.type.isdigit():
                # Numeric card: add its value to the score
                score += int(card.type)
            elif card.color != "":
                # Action cards: add 20 points to the score
                score += 20
            else:
                # Wildcards: add 50 points to the score
                score += 50

        return score

    def get_final_score(self) -> int:
        score = 0
        if self.get_winner().is_human:
            for player in self.players:
                score += self.get_hand_value(player)
        else:
            score = -self.get_hand_value(self.players[0])
        return score

    def next_turn(self):
        if self.has_ended():
            self.wait(1500)
            SoundManager.stop_bgm()
            winner = self.get_winner()
            score = self.get_final_score()            
            game_over_msg = InfoBox(
                f"Player {self.current_player_turn + 1} wins",
                [
                    [
                        TextElement(
                            text=f"Score: {score}"
                        )
                    ],
                    [
                        Button(
                            title="Main Menu",
                            callback=lambda: ScreenManager.return_to_main_menu()
                        ),
                        Button(
                            title="Exit to desktop",
                            callback=lambda: sys.exit()
                        )
                    ]
                ],
                has_close_button=False
            )
            if winner.is_human:
                SoundManager.win()
            else:
                SoundManager.lose()
            self.menu_manager.open_menu(game_over_msg)
        else:
            self.skip_turn()
            if not self.get_active_player().is_human:
                self.do_cpu_turn(self.get_active_player())

    def skip_turn(self):
        if self.clockwise:
            self.current_player_turn = (self.current_player_turn + 1) % self.max_players
        else:
            self.current_player_turn = self.current_player_turn - 1
            if self.current_player_turn < 0:
                self.current_player_turn = self.max_players - 1

    def reverse_turn_order(self):
        self.clockwise = not self.clockwise
        if self.max_players == 2:
            self.skip_turn()

    def do_cpu_turn(self, cpu: Player):
        self.wait(1000)
        for card in cpu.cards:
            if card.is_playable(self.discard_pile[-1]):
                cpu.play_card(card, 400)
                return
        self.deal_card(cpu, 1, 500)
        drawn_card = cpu.cards[-1]
        if drawn_card.is_playable(self.discard_pile[-1]):
            cpu.play_card(drawn_card, 400)
            return
        self.next_turn()

    def has_ended(self) -> bool:
        for p in self.players:
            if len(p.cards) == 0:
                return True
        return False
    
    def get_winner(self) -> Player:
        if self.has_ended():
            for p in self.players:
                if len(p.cards) == 0:
                    return p
        return None

    def popup_color_picker(self, draw: bool = False):
        self.deciding = True
        color_picker_menu = InfoBox(
            "Pick a color:",
            [
                [
                    Button(
                        title="Red",
                        text_color=pg.Color(255, 0, 0),
                        callback=lambda: self.change_top_card_color(0, draw)
                    ),
                    Button(
                        title="Green", 
                        text_color=pg.Color(0, 255, 0),
                        callback=lambda: self.change_top_card_color(1, draw)
                    ),
                ],
                [
                    Button(
                        title="Blue", 
                        text_color=pg.Color(0, 0, 255),
                        callback=lambda: self.change_top_card_color(2, draw)
                    ),
                    Button(
                        title="Yellow", 
                        text_color=pg.Color(255, 255, 0),
                        callback=lambda: self.change_top_card_color(3, draw)
                    )
                ]
            ],
            has_close_button=False
        )
        self.menu_manager.open_menu(color_picker_menu)

    def popup_bluff_challenge(self):
        self.deciding = True
        challenge_menu = InfoBox(
            position=pg.Vector2(self.screen.get_width() / 5, self.screen.get_height() / 2.5),
            title="What do you want to do?",
            element_grid=[
                [
                    Button(
                        title="Challenge",
                        text_color=pg.Color(255, 0, 0),
                        callback=lambda: self.apply_challenge_decision(True)
                    ),
                    Button(
                        title="Draw",
                        text_color=pg.Color(0, 128, 255),
                        callback=lambda: self.apply_challenge_decision(False)
                    )
                ]
            ],
            has_close_button=False
        )
        self.menu_manager.open_menu(challenge_menu)

    def apply_challenge_decision(self, d: bool):
        self.menu_manager.clear_menus()
        if d:
            SoundManager.challenge()
            self.get_previous_player().is_showing_hand = True
            self.wait(900)
            self.get_previous_player().is_showing_hand = False
            self.wait(100)
            # Check if the challenged player has a card with the same color as the card underneath the Wild +4.
            if self.get_previous_player().has_color(self.discard_pile[-2].color):
                SoundManager.challenge_success()
                self.wait(1500)
                # Successful challenge
                # The challenged player must draw 4. Then, is challenger's turn.
                SoundManager.force_draw(4)
                self.deal_card(self.get_previous_player(), 4)
                if not self.get_active_player().is_human:
                    self.do_cpu_turn(self.get_active_player())
            else:
                SoundManager.challenge_failed()
                self.wait(1500)
                # Failed challenge
                # The challenger must draw 6. Then, skips to the next player.
                SoundManager.force_draw(6)
                self.deal_card(self.get_active_player(), 6)
                self.next_turn()
        else:
            SoundManager.force_draw(4)
            self.deal_card(self.get_active_player(), 4)
            self.next_turn()

        self.deciding = False

    def change_top_card_color(self, color: int, draw: bool = False):
        self.discard_pile[-1].color = self.colors[color]
        self.discard_pile[-1].update_front()
        self.menu_manager.clear_menus()

        SoundManager.change_color()

        self.wait(1000)
        
        self.get_active_player().is_playing = False
        if draw:
            self.skip_turn()
            if self.house_rules & Rules.NO_BLUFFS != 0:
                self.apply_challenge_decision(False)
            else:
                if self.get_active_player().is_human:
                    self.popup_bluff_challenge()
                else:
                    self.apply_challenge_decision(random.randint(0, 1) == 1)
        else:
            self.next_turn()

        self.deciding = False

    def stack_plus_two(self):
        self.draw_stack += 2
        self.skip_turn()
        first_plus_two = self.get_active_player().get_first_card_of_type("D2")
        if first_plus_two and self.house_rules & Rules.STACKING != 0 and not self.has_ended():
            if not self.get_active_player().is_human:
                self.wait(1000)
                self.get_active_player().play_card(first_plus_two, 400)
        else:
            SoundManager.force_draw(self.draw_stack)
            self.deal_card(self.get_active_player(), self.draw_stack)
            self.draw_stack = 0
            self.next_turn()
    
    def uno_challenge(self, player: Player):
        SoundManager.challenge()
        self.wait(1000)
        SoundManager.force_draw(2)
        self.deal_card(player, 2)
    
    def get_player_with_identical_card(self) -> Player | None:
        for p in self.players:
            identical_card = p.get_identical_card()
            if identical_card:
                return p
        return None