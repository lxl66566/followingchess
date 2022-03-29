#coding=utf-8
import pygame
import numpy as np
from sys import exit
from pygame.locals import *
from math import floor,pi,round

__size_of_n = (6,30)
__base_size = 40                            #显示方格边长
__size_of_circle = (20,__base_size - 2)     #circle大小
direction = 0                               #风向
step = 0                                    #步数
biggest = 0                                 #当前格内最多

def relativepos_to_absolutepos(x,y) -> tuple:
    return ((x + 0.5) * __base_size,(y + 0.5) * __base_size)

def linear(x,y) -> list:
    temp = []
    for i in range(x - y,0,2):  #步长 =!= fps
        temp.append(round((lambda x: np.exp(-0.5 * x * x) / np.sqrt(2 * pi)) (i)))  #正态分布动画
    return temp

class circle:
    def __init__(self,pos:list,color:tuple,numb = 1,insist = True) -> None:
        self.pos = pos
        self.color = color
        self.numb = numb
        self.insist = insist
        self.update_radium()

    def update_radium(self):
        self.radium = (self.numb / biggest) * (__size_of_circle[1] - __size_of_circle[0]) + __size_of_circle[0]

    def draw_me(self):
        pygame.draw.circle(screen,self.color,relativepos_to_absolutepos(*self.pos),self.radium)

    def move_draw(self,to_pos:tuple) -> None:
        if self.pos[0] == to_pos[0]:
            temp = linear(self.pos[1],to_pos[1])


if __name__ == '__main__':
    while True:
        try:
            n = int(input('请输入一个[%d,%d]内的正整数表示棋盘大小：'%__size_of_n))
            if n < __size_of_n[0] or n > __size_of_n[1]:
                print('请按照数据范围输入！')
                continue
            break
        except ValueError:
            print('请按照格式输入！')
    if __base_size * (n + 2) >= 800:
        __base_size = floor(800 / (n + 2))

    pygame.init()
    screen = pygame.display.set_mode((__base_size * n, __base_size * (n + 2)), 0, 32)
    screen.fill((0,0,0))
    pygame.display.set_caption('followingchess_ made by |x|')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.flip()