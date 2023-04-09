 #By:
 	# Anuja Patil , Neethu Duggi , Vishwa Patel , Apurva Ratnaparkhi

from random import random
from tkinter import PhotoImage, Canvas
from enum import Enum, auto as enum_next
from math import pi
from typing import List, TYPE_CHECKING
from assets.Vectors import Vector2
from assets.AnimatedSprite import AnimatedSprite

if TYPE_CHECKING:
    from Sprites.Player import Player

class ZombiePriority(Enum):
    Moving = enum_next() 
    Attacking = enum_next()
    Idle = enum_next()

class Zombie(AnimatedSprite):
    FRAMES_ATTACK: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Zombie/skeleton-attack_{0}.png")
    FRAMES_ATTACK_CRITICAL_POINT = 0.55  
    FRAMES_IDLE: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Zombie/skeleton-idle_{0}.png")
    FRAMES_MOVE: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Zombie/skeleton-move_{0}.png")
    MAX_SPEED: float = 50 
    COLLIDER_WIDTH: float = 75

    def __init__(self, canvas: Canvas, target_player: "Player"):
        super().__init__(canvas, self.__class__.FRAMES_MOVE)
        self.target_player = target_player
        self.position = Vector2(1600 - self.halfImageSize.x, random() * 900)
        self.rotation = -pi / 2
        self.sqrDistToPlayer = 1600
        self.sqrDistToPlayerLimit = (self.__class__.COLLIDER_WIDTH + self.target_player.__class__.COLLIDER_WIDTH) ** 2
        self.speed = self.__class__.MAX_SPEED  # pixels per second
        self.cycleLength = 2
        self.__priority = ZombiePriority.Moving
        self.priority: ZombiePriority = ZombiePriority.Moving 
        self.hasAttacked = False
        self.hearts = 5

    @property
    def priority(self) -> ZombiePriority:
        return self.__priority

    @priority.setter
    def priority(self, new: ZombiePriority):
        if self.__priority != new:
            self.cycleTime = 0  
        self.__priority = new
        if new == ZombiePriority.Moving:
            self.frames = self.__class__.FRAMES_MOVE
        elif new == ZombiePriority.Attacking:
            self.frames = self.__class__.FRAMES_ATTACK
        elif new == ZombiePriority.Idle:
            self.frames = self.__class__.FRAMES_IDLE

    def update(self, dt):
        super(self.__class__, self).update(dt)
        displacement = self.target_player.position - self.position
        self.forwards = displacement
        self.sqrDistToPlayer: float = displacement.sqrMagnitude
        if self.sqrDistToPlayer < self.sqrDistToPlayerLimit:
            self.priority = ZombiePriority.Attacking
        if self.priority == ZombiePriority.Moving:
            self.position += self.forwards * (self.speed * dt)
        elif self.priority == ZombiePriority.Attacking:
            if not self.hasAttacked and self.sqrDistToPlayer < self.sqrDistToPlayerLimit \
                    and self.cycleTime >= self.cycleLength * self.__class__.FRAMES_ATTACK_CRITICAL_POINT:
                self.target_player.attacked()
                self.hasAttacked = True
                
    def shot(self) -> bool:
        self.hearts -= 1
        if self.hearts <= 0:
            self.destroyed = True
            return True
        return False                

    def cycleEnded(self):
        if self.priority != ZombiePriority.Attacking:
            return
        self.hasAttacked = False
        if self.sqrDistToPlayer > self.sqrDistToPlayerLimit:
            self.priority = ZombiePriority.Moving


