 #By:
 	# Anuja Patil , Neethu Duggi , Vishwa Patel , Apurva Ratnaparkhi
 	
from os.path import exists
from math import floor
from tkinter import PhotoImage, Canvas
from typing import Union, List
from assets.Vectors import Vector2
from assets.Sprite import Sprite

class AnimatedSprite(Sprite):
    def __init__(self, canvas: Canvas, frames: Union[List[PhotoImage], str],
                 cycle_length: float = 1, frame_interval: float = 0):
        if isinstance(frames, str):
            self.frames = AnimatedSprite.getFramesWithFilePattern(frames)
        else:
            self.frames = frames
        super().__init__(canvas, self.frames[0])
        self.imageSize = Vector2(self.image.width(), self.image.height())
        self.position = Vector2(0, 0)
        self.cycleTime: float = 0
        self.cycleLength = cycle_length
        self.frameInterval = frame_interval
        
    @property
    def frameInterval(self):
        return self._frameInterval

    @frameInterval.setter
    def frameInterval(self, new):
        if new > 0:
            self._frameInterval = new
            self._cycleLength = new * len(self.frames)

    @property
    def cycleLength(self):
        return self._cycleLength

    @cycleLength.setter
    def cycleLength(self, new):
        if new > 0:
            self._cycleLength = new
            self._frameInterval = new / len(self.frames)
  
    def update(self, dt):
        super(AnimatedSprite, self).update(dt)
        self.cycleTime += dt
        frame = floor(len(self.frames) * self.cycleTime / self.cycleLength)
        if frame >= len(self.frames):
            frame = 0
            self.cycleTime = 0
            self.cycleEnded()
        self.image = self.frames[frame]
        
    @staticmethod
    def getFramesWithFilePattern(file_pattern: str) -> List[PhotoImage]:
        i = 0
        frames: List[PhotoImage] = []
        while True:
            try:
                file = file_pattern.format(i)
                if not exists(file):
                    break  
                else:
                    frames.append(PhotoImage(file=file))
            finally:
                i += 1
        return frames

    def cycleEnded(self):
        pass


