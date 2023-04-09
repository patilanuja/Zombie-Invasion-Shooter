 #By:
 	# Anuja Patil , Neethu Duggi , Vishwa Patel , Apurva Ratnaparkhi

from math import sin, cos, atan2
from tkinter import Canvas
from assets.Vectors import Vector2

class ISprite:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.position = Vector2(0, 0)
        self.rotation: float = 0
        self._hidden: bool = False
        self.destroyed: bool = False
        self.needsANewDraw = True

    @property
    def forwards(self) -> Vector2:
        return self._forwards

    @forwards.setter
    def forwards(self, new: Vector2):
        self._forwards = new.normalise()
        self._rotation = atan2(new.x, new.y)

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, new: float):
        self._rotation = new
        self._forwards = Vector2(sin(new), cos(new))
        
    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, new: Vector2):
        self._pos = new
        self.validatePosition()

    def validatePosition(self):
        self.position.x = min(1600.0, max(self.position.x, 0))
        self.position.y = min(900.0, max(self.position.y, 0))


    def update(self, dt):
        pass

    @property
    def hidden(self):
        return self._hidden

    @hidden.setter
    def hidden(self, hidden: bool):
        if self._hidden == hidden:
            return 
        self._hidden = hidden
        if hidden:
            self.undraw()
        else:
            self.firstDraw()

    def firstDraw(self):
        self.needsANewDraw = False
        pass

    def redraw(self):
        if self.needsANewDraw:
            self.undraw()
            self.firstDraw()
        pass

    def undraw(self):
        pass


