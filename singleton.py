import os
from time import time
from hashlib import sha1
from tkinter import *
from datetime import date
from random import random

import pickle
from sprites.BossKeyBg import BossKeyBg
from sprites.Bullet import Bullets
from sprites.HealthIndicator import HealthIndicator
from sprites.Leaderboard import Leaderboard
from sprites.Player import Player
from sprites.ScoreIndicator import ScoreIndicator
from sprites.Zombie import Zombie
from assets.ISprite import ISprite
from assets.SavedState import SavedState
from assets.Sprite import Sprite
from assets.SpriteGroup import SpriteGroup
from assets.TextSprite import TextSprite
from assets.Vectors import Vector2
from typing import List
from game import *

class Singleton():
    _instance1='game'
    def _init_(self):
        """virtual private constructor"""
        if Singleton._instance1 !='game':
            raise Exception("This class is a singleton class !")
        else:
            Singleton._instance1 = self
 
    @staticmethod
    def getInstance():
        """Static Access Method"""
        if Singleton._instance1 == 'game':
            Singleton()
        return Singleton._instance1
