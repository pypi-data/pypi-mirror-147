#Bytes
import time
import sys
import os
import colorama
# colorama-0.4.4
RECT = "█"
RECT_1 = "▓"
RECT_2 = "▒"
RECT_3 = "░"
EMPTY = "   "
SCREEN = ""
EMPTY_1 = " "
EMPTY_2 = " "
BLOCK = "▂"
BLOCK_1 = "▬"
BLOCK_2 = "▆"
CORNER = "┏"
CORNER_1 = "┛"
CORNER_2 = "┓"
CORNER_3 = "┗"
BLOCK_3 = "━"
PIPE = "▏"
PIPE_1 = "▍"
PIPE_2 = "▋"
CLOSE = "╳"
MAXIM = "□"
MIN = "╸"
resolution = 600
fps = 1
class Screen:
    global SCREEN
    global RECT
    global RECT_1
    global EMPTY
    global RECT_2
    global RECT_3
    global fps
    global resolution
    resolution = 400
    fps = 2
    def __init__(self,fpsa,resolution):
        print("ConGUI initializated!")
        fps = fpsa
    #Screen
    def appendLine(self,sumbol):
        '''
        Appends line to console screen.
        '''
        global SCREEN
        
        SCREEN += sumbol + "\n"
    def append(self,sumbol):
        '''
        Appends sumbol to console screen.
        '''
        SCREEN += sumbol
    def wait(self):
        time.sleep(fps)
    def clearFrame(self):
        '''
        Clears frame,but works only on linux.
        '''
        SCREEN = "[2J"
    def test(self,rng):
        '''
        Used to test unicode charsets, idk why i added this :DD
        You can use it to check if your console gui application
        Supports unicode charset you want to use.
        '''
        for i in range(0,rng):
            sys.stdout.write(chr(i))        
    # https://stackoverflow.com/questions/54630766/how-can-move-terminal-cursor-in-python
    def setCursor(self,y, x):
        '''
        Sets cursor in terminal to x,y coordiates.
        '''
        print("\033[%d;%dH" % (y, x))
    #Animate
    def animation(self):
        '''
        Animates console screen and sets (fps) frames per second.
        '''
        while True:
            sys.stdout.write(SCREEN)
            time.sleep(1000/fps)
