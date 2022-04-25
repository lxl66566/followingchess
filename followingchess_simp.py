#coding=utf-8
import numbers
import pygame
from sys import exit
from pygame.locals import *
from math import floor,sqrt,atan,tan,pi,sin,cos
from copy import deepcopy
from random import randint

BLUE = (80,186,225)
ORANGE = (255,111,84)
WHITE = (255,255,255)
BLACK = (0,0,0)
SIZE = (9,30)
RADIUM_RATE = (0.5,0.95)
STANDARD_LENGTH = 40
WINDOWSIZE:list
WINDDIR = ((0,-1),(0,1),(-1,0),(1,0))
# WINDSIGNAL = ('↑','↓','←','→',' ')
WINDLEVEL = (1,4)
WINDSTART = 10      
VICTORY:int
biggest = 1
game = []
myfont:pygame.Surface
round = False        #True : blue False: orange
blow = 4
level = 0
chess_num = 0        #场上棋子数
gamestop = False
n:int

class circle:
    def __init__(self,pos:list,color,rad,num:int) -> None:
        self.pos = pos
        self.color = color
        self.rad = rad
        self.num = num
        self.font = pygame.font.Font(None,floor(STANDARD_LENGTH / 2))

    def draw_me(self,screen):
        pygame.draw.circle(screen,self.color,posmap(self.pos),self.rad)
        if self.num != 1:
            textImage = self.font.render(str(self.num),True,WHITE)
            text_pos = posmap(self.pos)
            text_pos[1] -= STANDARD_LENGTH * 0.12
            text_pos[0] -= 3
            if self.num > 9:
                text_pos -= 4
            screen.blit(textImage,text_pos)

    def update_rad(self):
        self.rad = floor(((self.num) / biggest * (RADIUM_RATE[1] - RADIUM_RATE[0]) + RADIUM_RATE[0]) * STANDARD_LENGTH / 2)

def posmap(pos):            #对位置的映射
    new_pos = list(pos)
    for i in range(2):
        new_pos[i] = new_pos[i] * STANDARD_LENGTH + floor(0.5 * STANDARD_LENGTH)
    return new_pos

def draw_line(screen):
    for i in range(n+1):
        pygame.draw.line(screen,BLACK,(0,STANDARD_LENGTH * i),(WINDOWSIZE[0],STANDARD_LENGTH * i))
    for i in range(1,n):
        pygame.draw.line(screen,BLACK,(STANDARD_LENGTH * i,0),(STANDARD_LENGTH * i,STANDARD_LENGTH * n))

def draw_arrow(screen,beginpos,endpos,length = 9,color = BLACK):                        #length是箭头末端的长度
    width_of_line = 2
    pygame.draw.line(screen,color,beginpos,endpos,width_of_line)
    try:
        k = (endpos[1] - beginpos[1]) / (endpos[0] - beginpos[0])
    except ZeroDivisionError:
        if endpos[1] < beginpos[1]:
            k = 0x7fffffff
        else:
            k = -0x7fffffff
    seita1 = atan(k) + pi/6
    seita2 = atan(k) - pi/6
    pos1 = [endpos[0] + cos(seita1) * length , endpos[1] + sin(seita1) * length]
    pos2 = [endpos[0] + cos(seita2) * length , endpos[1] + sin(seita2) * length]
    if endpos[0] > beginpos[0] and endpos[1] >= beginpos[1]:
        pos1 = [endpos[0] - cos(seita1) * length , endpos[1] - sin(seita1) * length]
        pos2 = [endpos[0] - cos(seita2) * length , endpos[1] - sin(seita2) * length]
    pygame.draw.line(screen,color,pos1,endpos,width_of_line)
    pygame.draw.line(screen,color,pos2,endpos,width_of_line)

def abs2rel(pos):
    output = list(pos)
    for i in range(2):
        output[i] = int(output[i] // STANDARD_LENGTH)
    return output

def update_chess_num():
    global chess_num
    chess_num = 0
    for i in game:
        for j in i:
            if j != []:
                chess_num += j[0].num

def draw(screen):
    global biggest
    blue   = circle([STANDARD_LENGTH * 1.5,(n + 1) * STANDARD_LENGTH],BLUE,  RADIUM_RATE[1] * STANDARD_LENGTH * 0.5,1)
    orange = circle([STANDARD_LENGTH * 3.5,(n + 1) * STANDARD_LENGTH],ORANGE,RADIUM_RATE[1] * STANDARD_LENGTH * 0.5,1)
    pygame.draw.circle(screen,blue.color,blue.pos,blue.rad)
    pygame.draw.circle(screen,orange.color,orange.pos,orange.rad)
    if round:
        triangle_pos = blue.pos
    else:
        triangle_pos = deepcopy(orange.pos)     #triangle_pos会修改orange.pos的值，所以需要deepcopy
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
            if j != [] and j[0].num > biggest:
                biggest = j[0].num
    draw_line(screen)
    for i in game:
        for j in i:
            if j == []:
                continue
            j[0].update_rad()
            j[0].draw_me(screen)
    myfont2 = pygame.font.Font(None,floor(RADIUM_RATE[1] * 0.8 * STANDARD_LENGTH))
    text_pos = orange.pos
    text_pos[0] += orange.rad + STANDARD_LENGTH * 0.8 * n / SIZE[1]
    text_pos[1] -= STANDARD_LENGTH * 0.2
    textImage = myfont2.render('blow:' + '       level:' + str(level),True,BLACK)
    screen.blit(textImage,text_pos)
    if blow < 4:
        arrow_pos = text_pos
        arrow_pos[0] += floor(RADIUM_RATE[1] * 0.8 * STANDARD_LENGTH * 2.4)
        arrow_pos[1] = blue.pos[1]
        length *= 0.9
        draw_arrow(screen,
                  (arrow_pos[0] - WINDDIR[blow][0] * length , arrow_pos[1] - WINDDIR[blow][1] * length) , 
                  (arrow_pos[0] + WINDDIR[blow][0] * length , arrow_pos[1] + WINDDIR[blow][1] * length),
                  18 * STANDARD_LENGTH / 40,(255,0,0))

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
    VICTORY = n * n * 3
    for i in range(n):
        game.append([])
        for j in range(n):
            game[i].append([])

    pygame.init()
    screen = pygame.display.set_mode(WINDOWSIZE, 0, 32)
    screen.fill(WHITE)
    pygame.display.set_caption('followingchess_simp made by |x|')

    draw(screen)
    next = 0
    while not gamestop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if next == 0:                           #下棋
                    pos = pygame.mouse.get_pos()
                    pos = abs2rel(pos)
                    if game[pos[0]][pos[1]] != []:
                        continue
                    color = ORANGE
                    if round:
                        color = BLUE
                    round = not round
                    game[pos[0]][pos[1]].append(circle(pos,color,1,1))
                    game[pos[0]][pos[1]][0].update_rad()
                    game[pos[0]][pos[1]][0].draw_me(screen)

                    update_chess_num()
                    if chess_num >= VICTORY:
                        gamestop = True
                    
                    if chess_num > WINDSTART:
                        next = 1
                        blow = randint(0,3)
                        level = randint(*WINDLEVEL)
                        for i in range(n):
                            for j in range(n):
                                if game[i][j] == []:
                                    continue
                                step = level
                                for dir in WINDDIR:
                                    if game[i + dir[0]][j + dir[1]] == []:
                                        continue
                                    try:
                                        if game[i + dir[0]][j + dir[1]][0].color is not color:
                                            step += game[i + dir[0]][j + dir[1]][0].num
                                        else:
                                            step -= game[i + dir[0]][j + dir[1]][0].num
                                    except IndexError:
                                        pass
                                if step < 1:
                                    step = 1
                                new_pos = (game[i][j][0].pos[0] + step * WINDDIR[blow][0] , 
                                          game[i][j][0].pos[1] + step * WINDDIR[blow][1])
                                if 0 <= new_pos[0] < n and 0 <= new_pos[1] < n:
                                    continue
                                draw_arrow(screen,posmap(game[i + dir[0]][j + dir[1]][0].pos), new_pos,color = game[i][j][0].color)
                                game[new_pos[0]][new_pos[1]].append(game[i][j][0])
                                game[i][j].pop(0)

                        for i in range(n):
                            for j in range(n):
                                if len(game[i][j]) <= 1:
                                    continue
                                blue = 0
                                orange = 0
                                for k in game[i][j]:
                                    if k.color == BLUE:
                                        blue += k.num
                                    else:
                                        orange += k.num
                                game[i][j].clear
                                if blue > orange:
                                    game[i][j].append(circle((i,j),BLUE,1,blue + orange))
                                elif orange > blue:
                                    game[i][j].append(circle((i,j),ORANGE,1,blue + orange))
                                else:
                                    continue
                                game[i][j][0].update_rad()
                                            

                elif next == 1:                         #下个回合
                    screen.fill(WHITE)
                    draw(screen)
                    next = 0


        pygame.display.update()