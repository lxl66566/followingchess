#coding=utf-8
from cmath import sqrt
from mimetypes import init
from select import select
import pygame
import numpy as np
from sys import exit
from pygame.locals import *
from math import floor

BLUE = (80,186,225)
ORANGE = (255,111,84)
WHITE = (255,255,255)
BLACK = (0,0,0)
SIZE = (6,30)
RADIUM_RATE = (0.5,0.95)
STANDARD_LENGTH = 40
WINDOWSIZE:list
WINDDIR = ((0,-1),(0,1),(-1,0),(1,0))
WINDLEVEL = (1,4)
biggest = 1
game = []
myfont = None
round = True        #True : blue False: orange
n:int

class circle:
    def __init__(self,pos:list,color,rad,num) -> None:
        self.pos = list(map(floor,pos))
        self.color = color
        self.rad = floor(rad)
        self.num = num

    def draw_me(self,screen):
        pygame.draw.circle(screen,self.color,posmap(self.pos),self.rad)
        if self.num != 1:
            textImage=myfont.render(str(self.num),True,BLACK)
            screen.blit(textImage,posmap(self.pos))

    def update_rad(self):
        self.rad = floor(((self.num - 1) / biggest * (RADIUM_RATE[1] - RADIUM_RATE[0]) + RADIUM_RATE[0]) * STANDARD_LENGTH / 2)

def posmap(pos):            #对位置的映射
    new_pos = pos
    for i in range(2):
        new_pos[i] = new_pos[i] * STANDARD_LENGTH + floor(0.5 * STANDARD_LENGTH)
    return new_pos

def draw_line(screen):
    for i in range(1,n+1):
        pygame.draw.line(screen,BLACK,(0,STANDARD_LENGTH * i),(WINDOWSIZE[0],STANDARD_LENGTH * i))
    for i in range(1,n):
        pygame.draw.line(screen,BLACK,(STANDARD_LENGTH * i,0),(STANDARD_LENGTH * i,STANDARD_LENGTH * n))

def draw(screen):
    global biggest
    blue = circle([STANDARD_LENGTH * 1.5,(n + 1) * STANDARD_LENGTH],BLUE,RADIUM_RATE[1] * STANDARD_LENGTH * 0.5,1)
    orange = circle([STANDARD_LENGTH * 3.5,(n + 1) * STANDARD_LENGTH],ORANGE,RADIUM_RATE[1] * STANDARD_LENGTH * 0.5,1)
    pygame.draw.circle(screen,blue.color,blue.pos,blue.rad)
    pygame.draw.circle(screen,orange.color,orange.pos,orange.rad)
    if round:
        triangle_pos = blue.pos
    else:
        triangle_pos = orange.pos
    triangle_pos[0] -= blue.rad + STANDARD_LENGTH * 0.3
    for i in range(2):
        triangle_pos[i] = floor(triangle_pos[i])
    length = floor(STANDARD_LENGTH * 0.5)
    pygame.draw.polygon(screen,(255,0,0),
                        [ triangle_pos ,
                        (floor(triangle_pos[0] - length * 1.7 / 2) , floor(triangle_pos[1] + length / 2)),
                        (floor(triangle_pos[0] - length * 1.7 / 2) , floor(triangle_pos[1] - length / 2))]
                        ,3)
    for i in game:
        for j in i:
            if j != 0 and j.num > biggest:
                biggest = j.num
    draw_line(screen)
    for i in game:
        for j in i:
            if j == 0:
                continue
            j.update_rad()
            j.draw_me(screen)
    myfont2 = pygame.font.Font(None,floor(RADIUM_RATE[1] * 0.5))


if __name__ == "__main__":
    while True:
        try:
            n = int(input(f'请输入一个[{SIZE[0]},{SIZE[1]}]内的正整数表示棋盘大小：'))
            if n < SIZE[0] or n > SIZE[1]:
                print('请按照数据范围输入！')
                continue
            break
        except ValueError:
            print('请按照格式输入！')

    WINDOWSIZE = [n * STANDARD_LENGTH , (n + 2) * STANDARD_LENGTH]
    if WINDOWSIZE[1] >= 800:
        STANDARD_LENGTH = floor(800 / (n + 2))
        WINDOWSIZE =  [n * STANDARD_LENGTH , (n + 2) * STANDARD_LENGTH]
    for i in range(n):
        game.append([])
        for j in range(n):
            game[i].append(0)

    pygame.init()
    screen = pygame.display.set_mode(WINDOWSIZE, 0, 32)
    screen.fill(WHITE)
    pygame.display.set_caption('followingchess_ made by |x|')
    myfont=pygame.font.Font(None,max(3,floor(STANDARD_LENGTH / 10)))

    draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        pygame.display.update()