 #By:
 	# Anuja Patil , Neethu Duggi , Vishwa Patel , Apurva Ratnaparkhi

from tkinter import NE
from typing import TYPE_CHECKING
from assets.Vectors import Vector2
from assets.TextSprite import TextSprite

if TYPE_CHECKING:
    from game import Game

class ScoreIndicator(TextSprite):
    POS_NORMAL = Vector2(1600-20, 0+20)
    POS_GAMEOVER = Vector2(1600*0.5, 900*0.2)
    def __init__(self, game: "Game"):
        super(ScoreIndicator, self).__init__(game.canvas)
        self.game: "Game" = game
        self.text = self.game.score
        self.options["font"] = 'Helvetica 30 bold'
        self.options["anchor"] = NE
        self.position = self.__class__.POS_NORMAL

    @TextSprite.position.getter
    def position(self) -> Vector2:
        return TextSprite.position.fget(self)

    @TextSprite.position.setter
    def position(self, position: Vector2):
        TextSprite.position.fset(self, position)
        font_size = 50 if position == self.__class__.POS_GAMEOVER else 30
        self.options["font"] = f'Helvetica {font_size} bold'

    def update(self, dt):
        if self.game.player.destroyed:
            return
        self.text = self.game.score
