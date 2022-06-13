from random import random
from random import randint
import pyxel

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

PLAYER_WIDTH = 24
PLAYER_HEIGHT = 5
PLAYER_SPEED = 5

GYOZA_WIDTH = 16
GYOZA_HEIGHT = 9
GYOZA_SPEED = 1.5

dokuGYOZA_WIDTH = 16
dokuGYOZA_HEIGHT = 9
dokuGYOZA_SPEED = 1.5

GYOZABY_WIDTH = 16
GYOZABY_HEIGHT = 9
GYOZABY_SPEED = 1.5

gyozas = []
dokugyozas = []
gyozabys = []

def update_list(list):
    for elem in list:
        elem.update()

def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.is_alive:
            list.pop(i)
        else:
            i += 1

def draw_list(list):
    for elem in list:
        elem.draw()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        self.is_alive = True

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += PLAYER_SPEED

        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - self.w)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 44, 56, self.w, self.h)

class Gyoza:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = GYOZA_WIDTH
        self.h = GYOZA_HEIGHT
        self.is_alive = True
        gyozas.append(self)

    def update(self):
        self.y += GYOZA_SPEED

    def draw(self):
        pyxel.blt(self.x, self.y, 1, 48, 53, self.w, self.h, 0)

class dokuGyoza:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = dokuGYOZA_WIDTH
        self.h = dokuGYOZA_HEIGHT
        self.is_alive = True
        dokugyozas.append(self)

    def update(self):
        self.y += dokuGYOZA_SPEED

    def draw(self):
        pyxel.blt(self.x, self.y, 1, 48, 69, self.w, self.h, 0)

class Gyozaby:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = GYOZABY_WIDTH
        self.h = GYOZABY_HEIGHT
        self.is_alive = True
        gyozabys.append(self)

    def update(self):
        self.y += GYOZABY_SPEED

    def draw(self):
        pyxel.blt(self.x, self.y, 1, 48, 86, self.w, self.h, 0)

class App:
    def __init__(self):
        pyxel.init(120, 160, title="tammy's gyoza bar")
        pyxel.load('my_resource.pyxres')
        self.scene = SCENE_TITLE
        self.score = 0
        self.player = Player(pyxel.width/2, pyxel.height - 20)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY

    def update_play_scene(self):
        if pyxel.frame_count % 12 == 0:
            tmp = randint(0,100)
            if tmp < 70:
                Gyoza(random() * (pyxel.width - PLAYER_WIDTH), 0)
            elif tmp >= 70 and tmp < 95:
                dokuGyoza(random() * (pyxel.width - PLAYER_WIDTH), 0)
            else : 
                Gyozaby(random() * (pyxel.width - PLAYER_WIDTH), 0)

        for gyoza in gyozas:
            if (
                gyoza.x+gyoza.w > self.player.x
                and self.player.x + self.player.w > gyoza.x
                and gyoza.y + gyoza.h > self.player.y
                and self.player.y + self.player.h > gyoza.y
            ):
                gyoza.is_alive = False
                pyxel.play(0,0,loop = False)
                self.score += 1
        
        for gyozaby in gyozabys:
            if (
                gyozaby.x+gyozaby.w > self.player.x
                and self.player.x + self.player.w > gyozaby.x
                and gyozaby.y + gyozaby.h > self.player.y
                and self.player.y + self.player.h > gyozaby.y
            ):
                gyozaby.is_alive = False
                pyxel.play(0,0,loop = False)
                self.score += 10

        for dokugyoza in dokugyozas:
            if (
                dokugyoza.x+dokugyoza.w > self.player.x
                and self.player.x + self.player.w > dokugyoza.x
                and dokugyoza.y + dokugyoza.h > self.player.y
                and self.player.y + self.player.h > dokugyoza.y
            ):
                dokugyoza.is_alive = False
                pyxel.play(1,1,loop=False)
                self.scene = SCENE_GAMEOVER

        for gyoza in gyozas:
            if (gyoza.y + gyoza.h > pyxel.height):
                gyoza.is_alive = False
                pyxel.play(1,1,loop=False)
                self.scene = SCENE_GAMEOVER

        for gyozaby in gyozabys:
            if (gyozaby.y + gyozaby.h > pyxel.height):
                gyozaby.is_alive = False
                pyxel.play(1,1,loop=False)
                self.scene = SCENE_GAMEOVER

        self.player.update()
        update_list(gyozas)
        update_list(dokugyozas)
        update_list(gyozabys)
        cleanup_list(gyozas)
        cleanup_list(dokugyozas)
        cleanup_list(gyozabys)

    def update_gameover_scene(self):
        update_list(gyozas)
        update_list(dokugyozas)
        update_list(gyozabys)
        cleanup_list(gyozas)
        cleanup_list(dokugyozas)
        cleanup_list(gyozabys)

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY
            self.player.x = pyxel.width / 2
            self.player.y = pyxel.height - 20
            self.score = 0
            gyozas.clear()
            dokugyozas.clear()
            gyozabys.clear()

    def draw(self):
        pyxel.cls(0)
        if self.scene == SCENE_TITLE:
            pyxel.bltm(-5, -50, 2, 0, 0, 130, 300, 1)
            self.draw_title_scene()
            pyxel.text(39,10, "SCORE     " + str(self.score), 0)
        elif self.scene == SCENE_PLAY:
            pyxel.bltm(35, 50, 3, 10, 10, 50, 60)
            self.draw_play_scene()
            pyxel.text(39,10, "SCORE     " + str(self.score), 7)
        elif self.scene == SCENE_GAMEOVER:
            pyxel.bltm(35, 50, 3, 10, 10, 50, 60)
            self.draw_gameover_scene()
            pyxel.text(39,10, "SCORE     " + str(self.score), 7)

    def draw_title_scene(self):
        pyxel.text(28, 60, "tammy's Gyoza bar", 8)
        pyxel.text(31, 140, "- PRESS ENTER -", 0)
    def draw_play_scene(self):
        self.player.draw()
        draw_list(gyozas)
        draw_list(dokugyozas)
        draw_list(gyozabys)
    def draw_gameover_scene(self):
         draw_list(gyozas)
         draw_list(dokugyozas)
         draw_list(gyozabys)
         pyxel.text(43, 40, "GAME OVER", 8)
         pyxel.text(31, 126, "- PRESS ENTER -", 13)

App()
