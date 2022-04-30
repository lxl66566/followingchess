#coding=utf-8
import pygame
from sys import exit
from math import floor,sqrt,atan,tan,pi,sin,cos,ceil
from copy import deepcopy
from random import randint
import os,json

VERSION = 'v1.1.0'
BLUE = (80,186,225)
ORANGE = (255,111,84)
WHITE = (255,255,255)
BLACK = (0,0,0)
SIZE = (9,30)
RADIUM_RATE = (0.5,0.95)
STANDARD_LENGTH = 40
WINDSTART = 6      
INF = 0x7fffffff
WINDOWSIZE:list
WINDDIR = ((0,-1),(0,1),(-1,0),(1,0))
WINDLEVEL = [1,4]
def update_windlevel():
    global WINDLEVEL
    WINDLEVEL[1] = max(1,ceil(min(sqrt(max(1,chess_num - 5 - biggest)) , n / 6.2)))#计算level随机上限
VICTORY:int     #一方超过另一方多少个子就算胜利
def get_victory():
    global VICTORY
    VICTORY = floor(n * 0.8)#调整vic-condition
biggest = 1
game = []
myfont:pygame.Surface
round = True        #True : blue False: orange
blow = 4
level = 0
chess_num = 0        #场上棋子数
chess_blue = 0
gamestop = False
n:int

class circle:
    def __init__(self,pos:list,color,rad,num:int) -> None:
        self.pos = pos
        self.color = color
        self.rad = rad
        self.num = num
        self.font = pygame.font.Font(None,floor(STANDARD_LENGTH / 2))
        self.new_pos = (INF,INF)

    def draw_me(self,screen):
        pygame.draw.circle(screen,self.color,posmap(self.pos),self.rad)
        if self.num != 1:
            textImage = self.font.render(str(self.num),True,WHITE)
            text_pos = posmap(self.pos)
            text_pos[1] -= STANDARD_LENGTH * 0.12
            text_pos[0] -= 3
            if self.num > 9:
                text_pos[0] -= 4
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
            k = INF
        else:
            k = -INF
    seita1 = atan(k) + pi/6
    seita2 = atan(k) - pi/6
    pos1 = [endpos[0] + cos(seita1) * length , endpos[1] + sin(seita1) * length]
    pos2 = [endpos[0] + cos(seita2) * length , endpos[1] + sin(seita2) * length]
    if endpos[0] > beginpos[0]:
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
    global chess_num,chess_blue
    chess_num = 0
    chess_blue = 0
    for i in game:
        for j in i:
            if j == []:
                continue
            chess_num += j[0].num
            if j[0].color == BLUE:
                chess_blue += j[0].num

def is_victory():
    blue = chess_blue
    orange = chess_num - blue
    if orange - blue >= VICTORY:
        return ORANGE
    elif blue - orange >= VICTORY:
        return BLUE
    else:
        return False

def victory(screen):
    global gamestop
    v = is_victory()
    if v == False:
        return
    gamestop = True
    screen.fill(WHITE)
    pos = [WINDOWSIZE[0] / 2,WINDOWSIZE[1] / 2]
    cir = circle(pos,v,RADIUM_RATE[1] * STANDARD_LENGTH,1)
    pygame.draw.circle(screen,cir.color,cir.pos,cir.rad)
    pos[1] += RADIUM_RATE[1] * STANDARD_LENGTH * 2
    pos[0] -= RADIUM_RATE[1] * STANDARD_LENGTH * 2
    myfont2 = pygame.font.Font(None,floor(RADIUM_RATE[1] * 2 * STANDARD_LENGTH))
    textImage = myfont2.render('WINS!',True,BLACK)
    screen.blit(textImage,pos)

def draw(screen):
    global biggest
    blue   = circle([STANDARD_LENGTH * 1.5,(n + 1) * STANDARD_LENGTH],BLUE,  RADIUM_RATE[1] * STANDARD_LENGTH * 0.5,1)
    orange = circle([STANDARD_LENGTH * 3.5,(n + 1) * STANDARD_LENGTH],ORANGE,RADIUM_RATE[1] * STANDARD_LENGTH * 0.5,1)
    pygame.draw.circle(screen,blue.color,blue.pos,blue.rad)
    pygame.draw.circle(screen,orange.color,orange.pos,orange.rad)

    update_chess_num()
    myfont3 = pygame.font.Font(None,floor(RADIUM_RATE[1] * 0.5 * STANDARD_LENGTH))
    chess_text_pos = [deepcopy(blue.pos),deepcopy(orange.pos)]
    for i in range(2):
        if i == 0:
            num = chess_blue
        else:
            num = chess_num - chess_blue
        textImage = myfont3.render(str(num),True,WHITE)
        text_pos = chess_text_pos[i]
        text_pos[1] -= STANDARD_LENGTH * 0.12
        text_pos[0] -= 3
        if num > 9:
            text_pos[0] -= 4
        screen.blit(textImage,text_pos)

    if round:
        triangle_pos = deepcopy(blue.pos)
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
    myfont2 = pygame.font.Font(None,floor(RADIUM_RATE[1] * 0.8 * STANDARD_LENGTH))  #大
    text_pos = deepcopy(orange.pos)
    text_pos[0] += orange.rad + STANDARD_LENGTH * 0.8 * n / SIZE[1]
    text_pos[1] -= STANDARD_LENGTH * 0.2
    textImage = myfont2.render(f'blow:       level:{level}',True,BLACK)
    screen.blit(textImage,text_pos)

    myfont2 = pygame.font.Font(None,floor(RADIUM_RATE[1] * 0.5 * STANDARD_LENGTH))  #小
    text_pos[1] -= STANDARD_LENGTH * 0.3
    textImage = myfont2.render('next',True,BLACK)
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

    text_pos = deepcopy(blue.pos)
    text_pos[1] += blue.rad + floor(0.15 * STANDARD_LENGTH)
    textImage = myfont2.render(f'vic-condition:{VICTORY}',True,BLACK)
    screen.blit(textImage,text_pos)


if __name__ == "__main__":
    try:
        with open(os.path.dirname(__file__) + os.sep + 'settings.json','r',encoding='utf-8') as f:
            settingdic = json.load(f)
    except FileNotFoundError:
        settingdic = {"randomarrows" : 1}
        with open(os.path.dirname(__file__) + os.sep + 'settings.json','w',encoding='utf-8') as f:
            json.dump(settingdic,f,indent=4)
    while True:
        try:
            n = int(input(f'请输入一个[{SIZE[0]},{SIZE[1]}]内的正整数表示棋盘大小：'))
            if n < SIZE[0] or n > SIZE[1]:
                print('请按照数据范围输入！')
                continue
            break
        except ValueError:
            print('请按照格式输入！')
    
    print(f'''
这里是 逐流棋 | {VERSION} 的规则：
游戏分为蓝方与橙方，交替下棋。当场上棋子数 >= {WINDSTART} 时开始流动，流动的方向与等级均随机。
棋子流动的规则是向指定方向流动 x 格(至少一格)，若流出边界则该棋子立刻失去联络。
x = level + 四周敌方棋子数 - 四周我方棋子数 - 当前格棋子数 + 1
当友方棋子流动到同一格时，数量叠加
当双方棋子流动到同一格时，多的吃少的（数量相等则湮灭）
胜利条件为双方棋子数量之差 >= 某一数值(vic-condition)
若要修改一些设置，请前往 README.txt 依照说明修改
    ''')

    WINDOWSIZE = [n * STANDARD_LENGTH , (n + 2) * STANDARD_LENGTH]
    if WINDOWSIZE[1] >= 800:
        STANDARD_LENGTH = floor(800 / (n + 2))
        WINDOWSIZE =  [n * STANDARD_LENGTH , (n + 2) * STANDARD_LENGTH]
    get_victory()
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
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if gamestop:
                    victory(screen)
                    continue
                if next == 0:                           #下棋
                    pos = pygame.mouse.get_pos()
                    pos = abs2rel(pos)
                    try:
                        if game[pos[0]][pos[1]] != []:#防乱点
                            break
                    except IndexError:
                        break
                    color = ORANGE
                    if round:
                        color = BLUE
                    game[pos[0]][pos[1]].append(circle(pos,color,1,1))
                    game[pos[0]][pos[1]][0].update_rad()
                    game[pos[0]][pos[1]][0].draw_me(screen)

                    update_chess_num()
                    victory(screen)

                    if chess_num == WINDSTART - 2 and not round:#4个棋,橙方落子后更新
                        blow = randint(0,3)
                        update_windlevel()
                        level = randint(*WINDLEVEL)

                    round = not round

                    if chess_num < WINDSTART:#不起风！
                        screen.fill(WHITE)  #切换当前回合玩家
                        draw(screen)
                        break

                    if not round:       #蓝方落子，不吹风
                        screen.fill(WHITE)
                        draw(screen)
                        break

                    next = 1
                    screen.fill(WHITE)
                    draw(screen)

                    for i in range(n):#检测新位置
                        for j in range(n):
                            if game[i][j] == []:
                                continue
                            step = deepcopy(level)
                            for dir in WINDDIR:
                                if i + dir[0] < 0 or j + dir[1] < 0:
                                    continue
                                try:
                                    if game[i + dir[0]][j + dir[1]] == []:
                                        continue
                                    if game[i + dir[0]][j + dir[1]][0].color is game[i][j][0].color:
                                        step -= game[i + dir[0]][j + dir[1]][0].num
                                    else:
                                        step += game[i + dir[0]][j + dir[1]][0].num
                                except IndexError:
                                    continue
                            step -= game[i][j][0].num - 1
                            if step < 1:
                                step = 1
                            new_pos = (game[i][j][0].pos[0] + step * WINDDIR[blow][0] , 
                                        game[i][j][0].pos[1] + step * WINDDIR[blow][1])
                            deal_pos = list(posmap(new_pos))
                            if settingdic["randomarrows"] != 0:
                                fence = ceil(STANDARD_LENGTH * RADIUM_RATE[1] * 0.27)
                                for k in range(2):
                                    deal_pos[k] += randint(-fence,fence)
                            draw_arrow(screen,posmap(game[i][j][0].pos), deal_pos ,color = game[i][j][0].color)
                            game[i][j][0].new_pos = new_pos
                    
                    for i in range(n):#移动
                        for j in range(n):
                            if game[i][j] == [] or game[i][j][0].new_pos == (INF,INF):
                                continue
                            new_pos = game[i][j][0].new_pos
                            for k in [1]:
                                if new_pos[0] < 0 or new_pos[1] < 0 :
                                    break
                                try:
                                    game[new_pos[0]][new_pos[1]].append(circle(new_pos,game[i][j][0].color,1,game[i][j][0].num))
                                    game[new_pos[0]][new_pos[1]][-1].update_rad()
                                except IndexError:
                                    pass
                            del(game[i][j][0])

                    for i in range(n):#查重
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
                            game[i][j].clear()
                            if blue > orange:
                                game[i][j].append(circle((i,j),BLUE,1,blue + orange))
                            elif orange > blue:
                                game[i][j].append(circle((i,j),ORANGE,1,blue + orange))
                            else:
                                continue
                            game[i][j][0].update_rad()
                                            

                elif next == 1:                         #下个回合
                    blow = randint(0,3)
                    update_windlevel()
                    level = randint(*WINDLEVEL)
                    
                    screen.fill(WHITE)
                    draw(screen)
                    next = 0


        pygame.display.update()