#coding=utf-8
import pygame
import numpy as np
from sys import exit
from pygame.locals import *
from math import floor,pi
# import asyncio

_size_of_n = (6,30)
_base_size = 40                             #显示方格边长
_size_of_circle = (20,_base_size - 2)       #circle大小
direction = 0                               #风向
step = 0                                    #步数
biggest = 1                                 #当前格内最多
_normal_distribution = []                   #动画移动比例表
_FPS = 2                                    #决定正态分布移动步长.
_asleep = 0.05                              #动画帧间隔
_V = 10                                     #10次循环移动一次
_BLUE = (80,186,225)
_ORANGE = (255,111,84)
_BACKGROUND = (255,255,255)

def relativepos_to_absolutepos(x,y) -> list:
    return [(x + 0.5) * _base_size,(y + 0.5) * _base_size]

def make_normal_list():
    for i in range(-350,0,_FPS): # i / 100
        _normal_distribution.append((lambda x: np.exp(-0.5 * x * x)) (i / 100))
    _normal_distribution.append(1)

class circle:
    def __init__(self,pos:list,color,numb = 1) -> None:
        self.pos:list = pos
        self.apos:list = relativepos_to_absolutepos(*pos)
        self.lastpos = self.apos
        self.color = color
        self.numb = numb
        self.update_radium()
        self.draw_me_relativepos()
        self.moving_step = len(_normal_distribution)        # len...,非移动中 0~n,移动第n步
        self.old_pos = []
        self.new_pos = []

    def update_radium(self):
        self.radium = (self.numb / biggest) * (_size_of_circle[1] - _size_of_circle[0]) + _size_of_circle[0]
        self.radium /= 2

    def draw_me_relativepos(self):
        self.apos = relativepos_to_absolutepos(*self.pos)
        self.draw_me_absolutepos()
    
    def draw_me_absolutepos(self):
        pygame.draw.circle(screen,_BACKGROUND,self.lastpos,self.radium)
        pygame.draw.circle(screen,self.color,self.apos,self.radium)
        self.last_pos = self.apos


def move_circle_a_step(c:circle):
    if c.moving_step == len(_normal_distribution):
        return
    xy = 0
    if c.old_pos[0] == c.new_pos[0]:                    #y向移动
        xy = 1
    c.apos[xy] = round(_normal_distribution[c.moving_step] * 
        (relativepos_to_absolutepos(*c.new_pos)[xy] - relativepos_to_absolutepos(*c.old_pos)[xy])
         + relativepos_to_absolutepos(*c.old_pos)[xy])
    c.draw_me_absolutepos()
    c.moving_step += 1

# def move_circles(list_of_circle:list):
#     stop = 1
#     t0 = time.process_time()
#     while stop:
#         if(time.process_time() - t0 < _asleep):
#             continue
#         else:
#             t0 = time.process_time()
#         stop = 0
#         for c in list_of_circle:
#             if c.moving_step == len(_normal_distribution):
#                 continue
#             stop = 1
#             move_circle_a_step(c)
#             c.moving_step += 1

if __name__ == '__main__':

    make_normal_list()

    while True:
        try:
            n = int(input(f'请输入一个[{_size_of_n[0]},{_size_of_n[1]}]内的正整数表示棋盘大小：'))
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
    screen.fill(_BACKGROUND)
    pygame.display.set_caption('followingchess_ made by |x|')

    test = [circle([1,1],_BLUE,1)]
    moving = False
    process = 0

    while True:
        if moving:
            process += 1
            if process % _V != 0:
                break
            stop_moving = True
            for i in test:
                if i.moving_step != _normal_distribution:
                    stop_moving = False
                    move_circle_a_step(i)
            if stop_moving:
                moving = False
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                moving = True
                process = -1
                test[0].old_pos = (1,1)
                test[0].new_pos = (1,6)
                test[0].moving_step = 0
