 #By:
 	# Anuja Patil , Neethu Duggi , Vishwa Patel , Apurva Ratnaparkhi
 	
from tkinter import PhotoImage
from enum import Enum, auto as enum_next
from math import pi, sin, cos, atan2
from typing import List, TYPE_CHECKING
from sprites.Bullet import Bullets
from assets.Vectors import Vector2
from assets.AnimatedSprite import AnimatedSprite

if TYPE_CHECKING:
    from game import Game
    from Sprites.Bullet import _Bullet
    
class _Gun(Enum):
    Handgun = enum_next()
    Shotgun = enum_next()

class Player(AnimatedSprite):
    FRAMES_IDLE_HANDGUN: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Player/handgun/idle/survivor-idle_handgun_{0}.png")
    FRAMES_MOVE_HANDGUN: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Player/handgun/move/survivor-move_handgun_{0}.png")
    MAX_SPEED: float = 100  
    COLLIDER_WIDTH: float = 50

    def __init__(self, game: "Game", bullets: Bullets):
        super().__init__(game.canvas, self.__class__.FRAMES_IDLE_HANDGUN) 
        self.game: Game = game
        self.bullets: Bullets = bullets
        self.position = Vector2(self.halfImageSize.x, 0.5 * 900)
        self.rotation = pi / 2
        self.inputUp = 0
        self.inputDown = 0
        self.inputLeft = 0
        self.inputRight = 0
        self.mousePos = Vector2(0.7, 0.5) * Vector2(1600, 900)
        self.gun: _Gun = _Gun.Handgun
        self.setupKeyBindings()
        self.activeCheatCodes: List[str] = []
        self.max_speed = self.__class__.MAX_SPEED  
        self.speed = 0  
        self.hearts = 5
        self.walkingRotation: float = pi / 2
        self.walkingDirection: Vector2 = Vector2(1, 0)

    def setupKeyBindings(self):
        controls = self.game.controls
        inputs = ("up", "left", "down", "right")
        for i in range(len(inputs)):
            self.game.tk.bind(f"<KeyPress-{controls[i]}>",
                              lambda e, kwarg=inputs[i]: self.setInput(**{kwarg: 1}))
            self.game.tk.bind(f"<KeyRelease-{controls[i]}>",
                              lambda e, kwarg=inputs[i]: self.setInput(**{kwarg: 0}))
        self.game.tk.bind('<Motion>', lambda e: self.setInput(mouse=Vector2(e.x, e.y)))
        self.game.tk.bind("<Button-1>", lambda e: self.shoot())

    def setInput(self, up: int = None, down: int = None, left: int = None, right: int = None, mouse: Vector2 = None):
        if up is not None:
            self.inputUp = up
        if down is not None:
            self.inputDown = down
        if left is not None:
            self.inputLeft = left
        if right is not None:
            self.inputRight = right
        if mouse is not None:
            self.mousePos = mouse

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, new):
        self._speed = new 
        self.cycleLength = max(1, new / 100)

    @property
    def gun(self) -> _Gun:
        return self._gun

    @gun.setter
    def gun(self, gun: _Gun):
        self._gun = gun
        if gun == _Gun.Handgun:
            self.framesIdle = self.__class__.FRAMES_IDLE_HANDGUN
            self.framesMove = self.__class__.FRAMES_MOVE_HANDGUN

    def shoot(self):
        if self.game.paused:
            return

        bulletDirection = self.mousePos - self.position
        if self.gun == _Gun.Shotgun:
            for i in range(3):
                bullet: "_Bullet" = self.bullets.newBullet(self.position, bulletDirection)
                bullet.rotation += (i-1) * 0.1  
        else:
            self.bullets.newBullet(self.position, bulletDirection)

    def update(self, dt):
        super(self.__class__, self).update(dt)
        dx = self.inputRight - self.inputLeft
        dy = self.inputDown - self.inputUp
        self.walkingRotation = atan2(dx, dy)
        self.walkingDirection = Vector2(sin(self.walkingRotation), cos(self.walkingRotation))
        self.forwards = self.mousePos - self.position
        self.position += self.walkingDirection * (self.speed * dt)
        if dx == 0 and dy == 0:
            if self.speed == 0:
                self.frames = self.framesIdle
            self.speed = 0
        else:
            if self.speed > 0:
                self.frames = self.framesMove
            self.speed = self.max_speed

    def attacked(self):
        self.hearts -= 1 
        if self.hearts <= 0:
            self.game.onGameOver()
            self.destroyed = True
