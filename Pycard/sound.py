import pygame as pg
import os.path

pg.mixer.init()

card_sound = pg.mixer.Sound(file=os.path.join("assets", "audio", "se", "sfx_card_play.wav"))
draw_sound = pg.mixer.Sound(file=os.path.join("assets", "audio", "se", "sfx_draw.wav"))
skip_sound = pg.mixer.Sound(file=os.path.join("assets", "audio", "se", "sfx_miss_turn.wav"))
reverse_sound = pg.mixer.Sound(file=os.path.join("assets", "audio", "se", "sfx_reverse.wav"))
draw_two_sound = pg.mixer.Sound(file=os.path.join("assets", "audio", "se", "sfx_draw_two.wav"))
color_change_sound = pg.mixer.Sound(file=os.path.join("assets", "audio", "se", "sfx_color_change.wav"))
illegal_move_sound = pg.mixer.Sound(file=os.path.join("assets", "audio", "se", "sfx_illegal_move.wav"))
challenge_sound = pg.mixer.Sound(file=os.path.join("assets", "audio", "se", "sfx_challenge.wav"))
challenge_success_sound = pg.mixer.Sound(file=os.path.join("assets", "audio", "se", "sfx_challenge_success.wav"))
challenge_failed_sound = pg.mixer.Sound(file=os.path.join("assets", "audio", "se", "sfx_challenge_failed.wav"))

button_sound = pg.mixer.Sound(file=os.path.join("assets", "audio", "se", "sfx_button.wav"))

yell_uno_voice = pg.mixer.Sound(file=os.path.join("assets", "audio", "va", "sfx_yell_uno.wav"))

win_voice = pg.mixer.Sound(file=os.path.join("assets", "audio", "va", "vfx_win.wav"))
win_jingle = pg.mixer.Sound(file=os.path.join("assets", "audio", "me", "victory.mp3"))

lose_voice = pg.mixer.Sound(file=os.path.join("assets", "audio", "va", "vfx_you_lose.wav"))
lose_jingle = pg.mixer.Sound(file=os.path.join("assets", "audio", "me", "defeat.mp3"))

draw_voices = [
    pg.mixer.Sound(file=os.path.join("assets", "audio", "va", "vfx_draw_two_player.wav")),
    pg.mixer.Sound(file=os.path.join("assets", "audio", "va", "vfx_draw_four_player.wav")),
    pg.mixer.Sound(file=os.path.join("assets", "audio", "va", "vfx_draw_six_player.wav")),
    pg.mixer.Sound(file=os.path.join("assets", "audio", "va", "vfx_draw_eight_player.wav")),
    pg.mixer.Sound(file=os.path.join("assets", "audio", "va", "vfx_draw_ten_player.wav")),
    pg.mixer.Sound(file=os.path.join("assets", "audio", "va", "vfx_draw_twelve_player.wav")),
    pg.mixer.Sound(file=os.path.join("assets", "audio", "va", "vfx_draw_fourteen_player.wav")),
    pg.mixer.Sound(file=os.path.join("assets", "audio", "va", "vfx_draw_sixteen_player.wav")),
    pg.mixer.Sound(file=os.path.join("assets", "audio", "va", "vfx_draw_eighteen_player.wav"))
]

class SoundManager:
    def main_menu():
        pg.mixer_music.load(filename=os.path.join("assets", "audio", "bgm", "main_menu.mp3"))
        pg.mixer_music.play(-1)
    def game_bgm(i: int):
        pg.mixer_music.load(filename=os.path.join("assets", "audio", "bgm", f"game{i}.mp3"))
        pg.mixer_music.play(-1)
    def stop_bgm():
        pg.mixer_music.stop()
    def play():
        card_sound.play()
    def draw():
        draw_sound.play()
    def skip():
        skip_sound.play()
    def reverse():
        reverse_sound.play()
    def force_draw(amount: int):
        draw_two_sound.play()
        draw_voices[amount // 2 - 1].play()
    def change_color():
        color_change_sound.play()
    def illegal_move():
        illegal_move_sound.play()
    def challenge():
        challenge_sound.play()
    def challenge_success():
        challenge_success_sound.play()
    def challenge_failed():
        challenge_failed_sound.play()
    def yell_uno():
        yell_uno_voice.play()
    def win():
        win_voice.play()
        win_jingle.play()
    def lose():
        lose_voice.play()
        lose_jingle.play()
    def button():
        button_sound.play()