#coding=utf-8
import pygame
import numpy as np
from sys import exit
from pygame.locals import *
from math import floor,pi
from time import sleep
import asyncio

_size_of_n = (6,30)
_base_size = 40                            #显示方格边长
_size_of_circle = (20,_base_size - 2)     #circle大小
direction = 0                               #风向
step = 0                                    #步数
biggest = 1                                 #当前格内最多
_BLUE = (80,186,225)
_ORANGE = (255,111,84)

def relativepos_to_absolutepos(x,y) -> list:
    return [(x + 0.5) * _base_size,(y + 0.5) * _base_size]

def linear(x,y) -> list:
    temp = []
    for i in range(x - y,0,2):  #步长 =!= fps
        temp.append(round((lambda x: np.exp(-0.5 * x * x) / np.sqrt(2 * pi)) (i)))  #正态分布动画
    return temp

class circle:
    def __init__(self,pos:list,color,numb = 1) -> None:
        self.pos:list = pos
        self.apos:list = relativepos_to_absolutepos(*pos)
        self.color = color
        self.numb = numb
        self.update_radium()
        self.update_rect()
        self.draw_me_relativepos()

    def update_rect(self) -> pygame.Rect:
        self.rect = pygame.Rect(self.apos[0] - self.radium,self.apos[1] - self.radium,self.apos[0] + self.radium,self.apos[1] + self.radium)
        return self.rect

    def update_radium(self):
        self.radium = (self.numb / biggest) * (_size_of_circle[1] - _size_of_circle[0]) + _size_of_circle[0]

    def draw_me_relativepos(self):
        self.apos = relativepos_to_absolutepos(*self.pos)
        self.draw_me_absolutepos()
    
    def draw_me_absolutepos(self):
        pygame.draw.circle(screen,self.color,self.apos,self.radium)
        pygame.display.update(self.update_rect())

    def move_draw(self,to_pos:list):
        xy = 0
        if self.pos[0] == to_pos[0]:                    #y向移动
            xy = 1
        elif self.pos[1] == to_pos[1]:                  #x向移动
            xy = 0
        temp = linear(self.pos[xy],to_pos[xy])
        for i in temp:
            self.apos[xy] = i
            oldrect = self.rect
            self.draw_me_absolutepos()
            pygame.display.update(oldrect)
            asyncio.sleep(0.1)
        self.pos = to_pos
        return True

async def mainprocess():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            await test.move_draw([1,9])
    pygame.display.update()


if __name__ == '__main__':

    while True:
        try:
            n = int(input('请输入一个[%d,%d]内的正整数表示棋盘大小：'%_size_of_n))
            if n < _size_of_n[0] or n > _size_of_n[1]:
                print('请按照数据范围输入！')
                continue
            break
        except ValueError:
            print('请按照格式输入！')
    if _base_size * (n + 2) >= 800:
        __base_size = floor(800 / (n + 2))

    pygame.init()
    screen = pygame.display.set_mode((_base_size * n, _base_size * (n + 2)), 0, 32)
    screen.fill((255,255,255))
    pygame.display.set_caption('followingchess_ made by |x|')


    test = circle([1,1],_BLUE,1)
    print(type(test.apos))
    while True:
        asyncio.run(mainprocess()) 