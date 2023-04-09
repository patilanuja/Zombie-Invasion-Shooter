 #By:
 	# Anuja Patil , Neethu Duggi , Vishwa Patel , Apurva Ratnaparkhi
 	
 	
from tkinter import * 	
import os
from random import random
from hashlib import sha1
from time import time
from datetime import date
from typing import List
import pickle
import pygame

tk = Tk()
pygame.init()

from sprites.ScoreIndicator import ScoreIndicator
from sprites.Zombie import Zombie
from sprites.BossKeyBg import BossKeyBg
from sprites.Leaderboard import Leaderboard
from sprites.Player import Player
from assets.ISprite import ISprite
from assets.SavedState import SavedState
from assets.TextSprite import TextSprite
from assets.Vectors import Vector2
from assets.Sprite import Sprite
from sprites.Bullet import Bullets
from sprites.HealthIndicator import HealthIndicator
from assets.SpriteGroup import SpriteGroup


INTERVAL_SECS_UPDATE = 1/60 
INTERVAL_SECS_REDRAW = 1/60  
MIN_DELAY = 0  
bg1 : PhotoImage = PhotoImage(file="images/Emojis/1.png")
bg2 : PhotoImage = PhotoImage(file="images/Emojis/2.png")
COLOR_GREY = "#494a49"
KEYS_INGNORED = ["Tab", "Alt_L", "Alt_R", "Shift_L", "Shift_R", "BackSpace"]  
KEYSYMS_REPR_ARROW = ["↑", "←", "↓", "→"]  
KEYSYMS_ARROW = ["Up", "Left", "Down", "Right"]  

def keysym_symbol_conversion(keysym: str):
    if keysym in KEYSYMS_ARROW:
        return KEYSYMS_REPR_ARROW[KEYSYMS_ARROW.index(keysym)]
    if len(keysym) == 1 and keysym.islower():
        return keysym.upper()
    return keysym


SAVE_FILE = "saves/save_{}.bin"


class Game: 
    ZOMBIE_SPAWN_COOLDOWN: int = 500
    def __init__(self, master):
        self.tk = master
        self.tk.geometry("1600x900")
        self.tk.resizable(False, False)
        self.canvas = Canvas(self.tk, width=1280, height=720, bg=COLOR_GREY, cursor="hand2", highlightthickness=0)
        self.canvas.pack(expand=YES, fill=BOTH)      
        self.started = False
        self.isGameOver: bool = False
        self.username = "User"
        self.controls: List[str] = ["w", "a", "s", "d"]
        self.sprites: List[ISprite] = []
        self.bullets = None
        self.player = None
        self.zombies = None
        self.score: int = 0
        self.scoreIndicator = None
        self.pausedIndicator = None
        self.bossKeyBg = None
        self.targetNumZombies: float = 0
        self.dontSpawnZombie: bool = True
        self.updateScheduled: bool = False
        self.redrawScheduled: bool = False
        self.paused: bool = True
        self.form()
        tk.bind('<Escape>', lambda e: self.toggle_paused())
        tk.bind('<Control-Escape>', lambda e: self.toggle_boss_key())
        tk.bind('<Return>', lambda e: self.re_start())
        tk.protocol("WM_DELETE_WINDOW", self.onClose)
        self.lastUpdateTime = time()

    def form(self):
        font = "Helvetica 15"
        self.canvas.create_image( 0, 0, image = bg1, anchor = "nw")
        self.canvas.create_text(800, 460, text="Welcome to 'Shoot At Sight'", fill="black", font=('Helvetica','30','bold'))
        self.canvas.create_text(800, 500, text="Please enter your name", fill="black", font=font)
        self.usernameInput = Entry(self.tk, width=23, font=font, justify=CENTER, bg="white")
        self.usernameInput.bind("<Return>", lambda e: self.submit_form())
        self.canvas.create_window(800, 550, window=self.usernameInput)
        self.usernameBtn = Button(self.tk, text="Start", bg="white", fg=COLOR_GREY, font="Helvetica 30", command=self.submit_form)
        self.canvas.create_window(800, 650, window=self.usernameBtn)
        self.controlsInputs = []
        controlsInputsPositions = ((800, 150), (700, 250), (800, 250),(900, 250))
        for i in range(len(self.controls)):
            entry = Entry(self.tk, width=2, font="Helvetica 50", justify=CENTER, bg="white")
            entry.insert(0, keysym_symbol_conversion(self.controls[i]))
            entry.configure(state="readonly")
            entry.bind("<KeyPress>", lambda e, entry=entry: self.input_controls(entry, e))
            entry.keysym = self.controls[i]
            self.controlsInputs.append(entry)
            self.canvas.create_window(*controlsInputsPositions[i], window=entry)                     
        self.usernameInput.focus_set()

    def start_all(self):
        self.started = True
        self.canvas.delete('all')
        self.canvas.create_image( 0, 0, image = bg2, anchor = "nw")
        del self.sprites
        self.isGameOver: bool = False
        self.sprites: List[ISprite] = []
        self.bullets = Bullets(self)
        self.sprites.append(self.bullets)
        self.player = Player(self, self.bullets)
        self.player.setupKeyBindings()
        self.sprites.append(self.player)
        self.zombies = SpriteGroup(self.canvas)
        self.sprites.append(self.zombies)
        self.sprites.append(HealthIndicator(self.canvas, self.player))
        self.score: int = 0
        self.scoreIndicator = ScoreIndicator(self)
        self.sprites.append(self.scoreIndicator)
        self.pausedIndicator = Sprite(self.canvas, "images/Emojis/23f8.png")
        self.pausedIndicator.position = Vector2(1600, 900) / 2
        self.sprites.append(self.pausedIndicator)
        self.bossKeyBg = BossKeyBg(self.canvas)
        self.sprites.append(self.bossKeyBg)
        self.targetNumZombies: float = 2.75
        self.dontSpawnZombie: bool = False
        self.loadState()
        self.paused = False

    def re_start(self):
        if not self.isGameOver:
            return
        else:
            self.start_all()

    def submit_form(self):
        if self.started:
            return
        username = self.usernameInput.get()
        if len(username) == 0:
            self.usernameInput.configure(bg="red")
            self.tk.after(300, lambda: self.usernameInput.configure(bg="white"))
            return
        self.username = username
        self.controls = [entry.keysym for entry in self.controlsInputs]
        self.paused = False

    def input_controls(self, entry: Entry, e):
        keysym = e.keysym
        if keysym in KEYS_IGNORED:
            return
        if len(keysym) == 1:
            keysym = keysym.lower()
        entry.keysym = keysym
        entry.configure(state=NORMAL)
        entry.delete(0, END)
        entry.insert(0, keysym_symbol_conversion(keysym))
        entry.configure(state="readonly")

    def update(self):
        startTime = time()
        dt = startTime - self.lastUpdateTime
        for sprite in self.sprites:
            sprite.update(dt)
        if not self.dontSpawnZombie and len(self.zombies.children) < self.targetNumZombies - 1:
            self.zombies.children.insertRight(Zombie(self.canvas, self.player))
            self.dontSpawnZombie = True
            self.tk.after(self.__class__.ZOMBIE_SPAWN_COOLDOWN, self._unlock_spawn)
        self.updateScheduled = False
        if not self.paused:
            self.lastUpdateTime = startTime
            remainingTime = INTERVAL_SECS_UPDATE - (time() - startTime)
            if remainingTime < MIN_DELAY:
                remainingTime = MIN_DELAY
            self.updateScheduled = True
            self.tk.after(int(remainingTime * 1000), self.update)

    def _unlock_spawn(self):
        self.dontSpawnZombie = False

    def redraw(self):
        startTime = time()
        for sprite in self.sprites:
            sprite.redraw()
        self.redrawScheduled = False
        if not self.paused:
            remainingTime = INTERVAL_SECS_REDRAW - (time() - startTime)
            if remainingTime < MIN_DELAY:
                remainingTime = MIN_DELAY
            self.redrawScheduled = True
            self.tk.after(int(remainingTime * 1000), self.redraw)

    def after_zombie_killed(self):
        self.targetNumZombies += 0.25
        self.score += 1

    def toggle_paused(self):
        self.paused = not self.paused

    def toggle_boss_key(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True
            self.pausedIndicator.hidden = True
            self.bossKeyBg.hidden = False

    @property
    def paused(self) -> bool:
        return self.__paused

    @paused.setter
    def paused(self, paused: bool):
        self.__paused = paused
        if not self.started:
            if not paused:
                self.start_all()
            return
        self.pausedIndicator.hidden = not self.paused
        self.bossKeyBg.hidden = True
        if not paused:
            self.lastUpdateTime = time()
            if not self.updateScheduled:
                self.updateScheduled = True
                self.update()
            if not self.redrawScheduled:
                self.redrawScheduled = True
                self.redraw()

    @property
    def usernameHash(self):
        return self._usernameHash

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, new: str):
        self._username = new
        self._usernameHash = sha1(self._username.encode("utf-8")).hexdigest()
           
    def loadState(self):
        try:
            with open(SAVE_FILE.format(self.usernameHash), "rb") as save_file:
                savedState: SavedState = pickle.load(save_file)
        except FileNotFoundError:
            return
        self.score = savedState.score
        self.targetNumZombies = savedState.targetNumZombies
        self.player.hearts = savedState.hearts
        self.player.position = savedState.playerPosition
        self.zombies.undraw()
        index = self.sprites.index(self.zombies)
        self.zombies = SpriteGroup(self.canvas)
        self.sprites[index] = self.zombies
        for i in range(len(savedState.zombiePositions)):
            zombie: Zombie = Zombie(self.canvas, self.player)
            zombie.position = savedState.zombiePositions[i]
            zombie.hearts = savedState.zombieHearts[i]
            zombie.cycleTime = random() * zombie.cycleLength  
            self.zombies.children.insertRight(zombie)
            
    def saveState(self):
        savedState: SavedState = SavedState(
            score=self.score,
            hearts=self.player.hearts,
            targetNumZombies=self.targetNumZombies,
            playerPosition=self.player.position,
            zombiePositions=[zombie.position for zombie in self.zombies.children],
            zombieHearts=[zombie.hearts for zombie in self.zombies.children],
            controls=self.controls)
        with open(SAVE_FILE.format(self.usernameHash), "wb") as save_file:
            pickle.dump(savedState, save_file)
            
    def onGameOver(self):
        if self.isGameOver:
            return
        self.isGameOver = True
        self.paused = True
        self.pausedIndicator.hidden = True
        self.sprites.append(Leaderboard(self.canvas, self.score, date.today().strftime("%d-%m-%Y"), self.username))
        self.scoreIndicator.position = ScoreIndicator.POS_GAMEOVER
        self.canvas.create_text(800, 130, text="Thank you! Happy Halloween :)", fill="black", font=('Helvetica','30','bold'))
        hintText = TextSprite(self.canvas, text="Press Enter to play again!!")
        hintText.position = Vector2(1600*0.5, 900*0.8)
        self.sprites.append(hintText)
        try:
            os.remove(SAVE_FILE.format(self.usernameHash))
        except FileNotFoundError:
            pass

    def onClose(self):
        if not self.started or not self.isGameOver:
            self.saveState()
        self.tk.destroy()

if __name__ == "__main__":
    game = Game(tk)
    tk.mainloop()
