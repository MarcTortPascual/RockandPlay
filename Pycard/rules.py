class Rules:
    # Allows +2 being stacked with other +2.
    STACKING = 1
    # Adds an extra behaviour when you play a seven: you must switch your hand with another player.
    # Also, if you play a zero, all the players must give his hand to his next player.
    SEVEN_O = 2
    # Allows to play an identical card (i.e., a blue 7 onto another blue 7), even outside of the player's turn.
    INTERCEPT = 4
    # Forces the player to play the drawn card, if playable.
    FORCE_PLAY = 8
    # Disables the Wild +4 bluffs, meaning that you can play a Wild +4 illegally.
    NO_BLUFFS = 16
    # Forces the player to draw until draws a playable card.
    DRAW_UNTIL_PLAY = 32