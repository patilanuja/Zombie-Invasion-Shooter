 #By:
 	# Anuja Patil , Neethu Duggi , Vishwa Patel , Apurva Ratnaparkhi

from tkinter import Canvas
from assets.Vectors import Vector2
from assets.ISprite import ISprite

class TextSprite(ISprite):
    def __init__(self, canvas: Canvas, text: str = ""):
        self.text = text
        self.options = {
            "fill": "white",
            "font": "Helvetica 16 bold"}
        self.canvas_text = "None"
        super(TextSprite, self).__init__(canvas)
        
    @ISprite.position.setter
    def position(self, new: Vector2):
        ISprite.position.fset(self, new)
        self.needsANewDraw = True
        
    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, new: str):
        self.__text = new
        self.needsANewDraw = True



    def firstDraw(self):
        super(TextSprite, self).firstDraw()
        self.canvas_text = self.canvas.create_text(*self.position, text=self.text, **self.options)

    def redraw(self):
        super(TextSprite, self).redraw()
        pass
    
    def undraw(self):
        super(TextSprite, self).undraw()
        self.canvas.delete(self.canvas_text)
