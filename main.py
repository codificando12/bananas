import tkinter as tk
from tkinter import PhotoImage, Canvas
import ctypes
import pyautogui
import random

class Banana():
    def __init__(self, scene, x=0, y=0):
        self.scene = scene
        self.image = PhotoImage(file='C:\\Users\\eciap\\Documents\\GitHub\\bananas\\banana.png')
        self.image = self.image.subsample(16)
        self.imageRef = scene.canvas.create_image(x, y, image=self.image)
        self.banana_touch = False

    def update(self):
        x, y = pyautogui.position()
        ban_x, ban_y = self.scene.canvas.coords(self.imageRef)
        dist =(abs(x-ban_x) + abs(y-ban_y))
        if self.banana_touch:
            self.scene.canvas.move(
                self.imageRef,
                random.choice((-30, 30)),
                random.choice((-30,30))
            )
            self.scene.new_banana(
                random.randint(0, self.scene.screen_width),
                random.randint(0, self.scene.screen_heigth)
            )
            self.banana_touch = False
        elif dist < 5:
            self.banana_touch = True
        else:
            self.scene.canvas.move(
                self.imageRef,
                1 if x > ban_x else -1,
                1 if y > ban_y else -1
            )

class Scene():
    def __init__(self, window: tk.Tk):
        self.screen_width = window.winfo_screenwidth()
        self.screen_heigth = window.winfo_screenheight()
        self.canvas = Canvas(
            window,
            width=self.screen_width,
            height=self.screen_heigth,
            highlightthickness=0,
            bg='white'
            )
        self.canvas.pack()
        self.bananas = list()

    def update(self):
        for banana in self.bananas:
            banana.update()

    def new_banana(self, x, y):
        banana = Banana(self)
        self.canvas.move(banana.imageRef, x, y)
        self.bananas.append(banana)

class Game():
    def __init__(self):
        self.window =self.create_window()
        self.apply_click_through(self.window)
        self.scene =Scene(self.window)

    def update(self):
        self.scene.update()
        self.window.after(20,self.update)

    def create_window(self):
        window = tk.Tk()
        window.wm_attributes("-topmost", True)
        window.attributes("-fullscreen", True)
        window.overrideredirect(True)
        #transparent color
        window.attributes('-transparentcolor', 'white')
        window.config(bg='white')
        return window
    
    def apply_click_through(self, window):
        #constan Windows API
        WS_EX_TRANSPARENT = 0X00000020
        WS_EX_LAYERED = 0x00080000
        GWL_EXSTYLE = -20

        #Find windows identificator (HWND)
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)

        #new style
        style = style | WS_EX_TRANSPARENT | WS_EX_LAYERED
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

    def start(self):
        self.update()
        self.window.mainloop()

game = Game()
game.scene.new_banana(100,100)
game.start()
