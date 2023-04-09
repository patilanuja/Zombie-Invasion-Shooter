 #By:
 	# Anuja Patil , Neethu Duggi , Vishwa Patel , Apurva Ratnaparkhi

from tkinter import Canvas
from assets.Vectors import Vector2
from assets.Sprite import Sprite

class BossKeyBg(Sprite):
    def __init__(self, canvas: Canvas):
        super(BossKeyBg, self).__init__(canvas, "images/BossKeyBg.png")
        self.position = Vector2(1600, 900) / 2
        self.hidden = True

    def redraw(self):
        self.canvas.tag_raise(self.canvas_image)
        
