 #By:
 	# Anuja Patil , Neethu Duggi , Vishwa Patel , Apurva Ratnaparkhi

from tkinter import PhotoImage, Canvas, NW
from typing import TYPE_CHECKING
from assets.ISprite import ISprite

if TYPE_CHECKING:
    from Sprites.Player import Player

HEART_FULL: PhotoImage = PhotoImage(file="images/Emojis/pumpkin.png")
HEART_BROKEN: PhotoImage = PhotoImage(file="images/Emojis/1f494.png")
HEART_SIZE: int = 32
HEART_PADDING: int = 5

class HealthIndicator(ISprite):
    def __init__(self, canvas: Canvas, player: "Player"):
        super().__init__(canvas)
        self.player: "Player" = player
        self.maxHearts: int = self.player.hearts  
        self.drawnHearts: int = 0
        self.canvas_hearts: list = []

    def firstDraw(self):
        super(HealthIndicator, self).firstDraw()
        self.canvas_hearts = []
        x = 20
        for i in range(self.maxHearts):
            image = HEART_FULL if self.player.hearts > i else HEART_BROKEN
            self.canvas_hearts.append(self.canvas.create_image(x, 20, image=image, anchor=NW))
            x += HEART_SIZE + HEART_PADDING
        self.drawnHearts = self.player.hearts

    def redraw(self):
        super(HealthIndicator, self).redraw()
        if self.player.hearts != self.drawnHearts:  
            self.undraw()
            self.firstDraw()

    def undraw(self):
        super(HealthIndicator, self).undraw()
        for heart in self.canvas_hearts:
            self.canvas.delete(heart)
