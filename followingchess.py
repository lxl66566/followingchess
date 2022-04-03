#coding=utf-8
import imp
from time import sleep
import pygame
import numpy as np
from sys import exit
from pygame.locals import *
from math import floor,pi
import time
# import asyncio

_size_of_n = (6,30)
_base_size = 40                            #显示方格边长
_size_of_circle = (20,_base_size - 2)     #circle大小
direction = 0                               #风向
step = 0                                    #步数
biggest = 1                                 #当前格内最多
_normal_distribution = []                   #动画移动比例表
_FPS = 2                                    #决定正态分布移动步长.
_asleep = 0.05                               #动画帧间隔
_BLUE = (80,186,225)
_ORANGE = (255,111,84)

def relativepos_to_absolutepos(x,y) -> list:
    return [(x + 0.5) * _base_size,(y + 0.5) * _base_size]

def make_normal_list():
    for i in range(-350,0,_FPS): # i / 100
        _normal_distribution.append((lambda x: np.exp(-0.5 * x * x)) (i / 100))
    _normal_distribution.append(1)

# def linear(x,y):
#     temp = []
#     for i in _normal_distribution:
#         temp.append(round(i * (y - x) + x)) #正态分布动画
#     return temp

class circle:
    def __init__(self,pos:list,color,numb = 1) -> None:
        self.pos:list = pos
        self.apos:list = relativepos_to_absolutepos(*pos)
        self.color = color
        self.numb = numb
        self.update_radium()
        # self.update_rect()
        self.draw_me_relativepos()
        self.moving_step = len(_normal_distribution)        # len...,非移动中 0~n,移动第n步
        self.old_pos = []
        self.new_pos = []

    # def update_rect(self) -> pygame.Rect:
    #     self.rect = pygame.Rect(self.apos[0] - self.radium,self.apos[1] - self.radium,self.apos[0] + self.radium,self.apos[1] + self.radium)
    #     return self.rect

    def update_radium(self):
        self.radium = (self.numb / biggest) * (_size_of_circle[1] - _size_of_circle[0]) + _size_of_circle[0]
        self.radium /= 2

    def draw_me_relativepos(self):
        self.apos = relativepos_to_absolutepos(*self.pos)
        self.draw_me_absolutepos()
    
    def draw_me_absolutepos(self):
        pygame.draw.circle(screen,self.color,self.apos,self.radium)
        # pygame.display.update(self.update_rect())       #新位置自动更新

def move_circle_a_step(c:circle):
    xy = 0
    if c.old_pos[0] == c.new_pos[0]:                    #y向移动
        xy = 1
    c.apos[xy] = round(_normal_distribution[c.moving_step] * (c.new_pos[xy] - c.old_pos[xy]) + c.old_pos[xy])
    c.draw_me_absolutepos()

def move_circles(list_of_circle:list):
    stop = 1
    t0 = time.process_time()
    while stop:
        if(time.process_time() - t0 < _asleep):
            continue
        else:
            t0 = time.process_time()
        stop = 0
        for c in list_of_circle:
            if c.moving_step == len(_normal_distribution):
                continue
            stop = 1
            move_circle_a_step(c)
            c.moving_step += 1
        
        # asyncio.sleep(_asleep)


# def move_draw(self,to_pos:list):
#     xy = 0
#     if self.pos[0] == to_pos[0]:                    #y向移动
#         xy = 1
#     elif self.pos[1] == to_pos[1]:                  #x向移动
#         xy = 0
#     temp = linear(self.pos[xy],to_pos[xy])
#     for i in temp:
#         self.apos[xy] = i
#         oldrect = self.rect
#         self.draw_me_absolutepos()
#         pygame.display.update(oldrect)
#     self.pos = to_pos
#     return True

if __name__ == '__main__':

    make_normal_list()

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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                test.old_pos = relativepos_to_absolutepos(1,1)
                test.new_pos = relativepos_to_absolutepos(1,6)
                test.moving_step = 0
                move_circles([test])

        pygame.display.update()