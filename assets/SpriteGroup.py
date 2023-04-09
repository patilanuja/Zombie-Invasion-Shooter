 #By:
 	# Anuja Patil , Neethu Duggi , Vishwa Patel , Apurva Ratnaparkhi

from tkinter import Canvas
from assets.LinkedList import LinkedList
from assets.ISprite import ISprite

class SpriteGroup(ISprite):
    def __init__(self, canvas: Canvas):
        super().__init__(canvas)
        self.children: LinkedList = LinkedList()

    def update(self, dt):
        self.children.removeWith(
            shouldRemove=lambda node: node.element.destroyed,
            onRemove=lambda child: self.removeChild(child),
            removeAll=True)
        for child in self.children:
            child.update(dt)

    def removeChild(self, child: ISprite):
        child.hidden = True

    def firstDraw(self):
        super(SpriteGroup, self).firstDraw()
        for child in self.children:
            child.firstDraw()

    def undraw(self):
        for child in self.children:
            child.undraw()
            
    def redraw(self):
        super(SpriteGroup, self).redraw()
        for child in self.children:
            child.redraw()

