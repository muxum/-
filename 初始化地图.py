########引入包############
import pygame, os
from pygame.locals import *
import random
import numpy as np
import copy
#########引入宏##############
######显示宏###
RUN = True
#####END#####
SIZE_SCREEN = (450, 450)  # 屏幕尺寸
######颜色
QP_C = (200, 200, 200)
ROAD_C = (255, 250, 250)
#####END
INF = 1000
#####迷宫尺寸
STEP = 50  # 迷宫的阶数
MAPRANK = STEP
MAPCROSS = STEP
X = 0  # 迷宫起始横坐标
Y = 0  # 迷宫起始纵坐标
BS = min(SIZE_SCREEN)//STEP  # 方格尺寸
# 线宽
RWW = 2  # 迷宫线宽
####END
####主体
C = 5
customers = []
R = 3
restaurants = []
W = 3
waiter = []
#####END
pygame.init()
screen = pygame.display.set_mode(SIZE_SCREEN)
pygame.display.set_caption("外卖模拟系统")
screen.fill(QP_C)
def buildmap(STEP):
    w = STEP

    MAP = np.ones((w, w), dtype=int)
    MAP = MAP.dot(INF)
    mark = np.zeros((w, w), dtype=int)

    lis = [(0, 1, 0),
           (0, 0, 1),
           (1, 0, 0)]

    mark[0][0] = 1

    while True:

        if len(lis) == 0:
            break

        x = random.choice(lis)
        a = x[0]
        b = x[1]
        c = x[2]

        if (a == 0 and c == 0) or (a == w - 1 and c == 2) or (b == 0 and c == 3) or (b == w - 1 and c == 1):
            lis.remove(x)
            continue

        if c == 0:
            a1 = a - 1
            b1 = b
        if c == 1:
            a1 = a
            b1 = b + 1
        if c == 2:
            a1 = a + 1
            b1 = b
        if c == 3:
            a1 = a
            b1 = b - 1

        d = (c + 2) % 4

        if mark[a][b] == 0 or mark[a1][b1] == 0:

            if mark[a][b] == 0:
                for i in range(4):
                    if i != c:
                        lis.append((a, b, i))

            if mark[a][b] == 1:
                for i in range(4):
                    if i != d:
                        lis.append((a1, b1, i))

                lis.remove((a, b, c))

                # MAP[a][b][c] = 1
                # MAP[a1][b1][d] = 1

                MAP[a][b] = 1

                mark[a1][b1] = 1

        else:
            lis.remove((a, b, c))
    print(MAP)
    return MAP

def F(GX_C, GY_C, MX_C, MY_C, g):
    global MAP
    h = (abs(GY_C - MY_C) + abs(GX_C - MX_C))
    f = g + h
    return g, h, f
def _A(MX_C, MY_C, gx, gy, gmap):
    BACKX = -1
    BACKY = -1
    GX_C = gx
    GY_C = gy
    # 0.把当前节点放入OPEN
    f = F(GX_C, GY_C, MX_C, MY_C, 0)[2]
    OPEN = {}
    OPEN[GX_C, GY_C, 0] = f
    CLOSE = {}
    father = {}
    father[GX_C, GY_C, 0] = 0
    # 1.判断表非空
    while OPEN:
        # 2.表第一个节点放入close
        # 7.代价最小的删除OPEN表加入CLOSE表
        n = sorted(OPEN.items(), key=lambda d: d[1])
        CLOSE[n[0][0]] = n[0][1]

        del OPEN[n[0][0]]
        GX_C = n[0][0][0]
        GY_C = n[0][0][1]
        g = n[0][0][2]
        # 3.n为目标节点？

        if GX_C == MX_C and GY_C == MY_C:
            BACKX, BACKY, bg = GX_C, GY_C, g
            break
        # 4.n可拓展？
        # 可走的节点里没有我爸爸
        # 5找出子节点加入open表father:键值对-》儿子：爸爸
        # 6.计算各节点代价
        if GY_C + 1< MAPCROSS:
            if gmap[GX_C][GY_C+1] != INF and (GX_C, GY_C + 1, g - 1) != father[GX_C, GY_C, g]:  # 右
                f1 = F(GX_C, GY_C + 1, MX_C, MY_C, g + 1)[2]
                if (GX_C, GY_C + 1, g + 1) not in OPEN:
                    OPEN[GX_C, GY_C + 1, g + 1] = f1
                    father[GX_C, GY_C + 1, g + 1] = (GX_C, GY_C, g)
        if  GY_C - 1 >=0:
            if gmap[GX_C][GY_C-1] != INF and (GX_C, GY_C - 1, g - 1) != father[GX_C, GY_C, g]:  # 左
                f3 = F(GX_C, GY_C - 1, MX_C, MY_C, g + 1)[2]
                if (GX_C, GY_C - 1, g + 1) not in OPEN:
                    OPEN[GX_C, GY_C - 1, g + 1] = f3
                    father[GX_C, GY_C - 1, g + 1] = (GX_C, GY_C, g)
        if GX_C + 1 < MAPRANK:
            if gmap[GX_C+1][GY_C] != INF and (GX_C + 1, GY_C, g - 1) != father[GX_C, GY_C, g]:  # 下
                f2 = F(GX_C + 1, GY_C, MX_C, MY_C, g + 1)[2]
                if (GX_C + 1, GY_C, g + 1) not in OPEN:
                    OPEN[GX_C + 1, GY_C, g + 1] = f2
                    father[GX_C + 1, GY_C, g + 1] = (GX_C, GY_C, g)
        if GX_C - 1 >= 0:
            if gmap[GX_C-1][GY_C] != INF and (GX_C - 1, GY_C, g - 1) != father[GX_C, GY_C, g]:  # 上
                f0 = F(GX_C - 1, GY_C, MX_C, MY_C, g + 1)[2]
                if (GX_C - 1, GY_C, g + 1) not in OPEN:
                    OPEN[GX_C - 1, GY_C, g + 1] = f0
                    father[GX_C - 1, GY_C, g + 1] = (GX_C, GY_C, g)
    # 找爸爸
    back = []
    if BACKX != -1 and BACKY != -1:
        back = []
        back.append((BACKX, BACKY))
        while father[BACKX, BACKY, bg] != 0:
            wk = father[BACKX, BACKY, bg]
            BACKX = wk[0]
            BACKY = wk[1]
            bg = wk[2]
            back.append((BACKX, BACKY))
        back = list(reversed(back))#返回的是从起点指向终点的路径
        del back[0]
        return back
    else:
        print("error")
        back = [(0, 0)]
        return back
    return

def _navigation(MAP, BS, back):
    # 画网格线
    for i in range(MAPRANK):
        for j in range(MAPCROSS):
            if MAP[i][j] == INF:
                    pygame.draw.rect(screen, ROAD_C,
                        ((X + j*BS, Y+ i*BS), (BS, BS)),
                        0)
        # 画出图
    for i in range(C+R):
        for j in range(C+R):
            if edge[i][j] != 0:
                for e in edge[i][j]:
                    pygame.draw.rect(screen, (255,250, 3),
                                     ((X + e[1] * BS, Y + e[0] * BS), (BS, BS)),
                                     0)
    # 画出顾客
    for c in range(len(customers)):
        screen.blit(pygame.font.Font('freesansbold.ttf',
                                    15).render(f"{c+1}", True, (255, 0, 0)),
                    (X + customers[c][1]* BS + BS // 2, Y + customers[c][0]* BS + BS // 2 ) )
    #画出饭店
    for r in range(len(restaurants)):
        screen.blit(pygame.font.Font('freesansbold.ttf',
                                     20).render(f"{r + 1}", True, (230, 5, 250)),
                    (X + restaurants[r][1] * BS + BS // 2, Y + restaurants[r][0] * BS + BS // 2))
# 函数主体
#"""

#    """
MAP = buildmap(STEP)

global end_x,end_y,road
maze = MAP
#print(MAP)
row,col = np.shape(maze)
print(row,col)
ran = np.zeros((row,col))

"""
#ran 是与maze一般大小的矩阵。-1表示C的位置，-2表示R的位置，可以用来构建CR图
#CR图，是C与R之间的连通图，任意两CC\RR\CR之间都有一个节点，在CR生成后存入数据库
在求TSP时，从CR图中调出需要的行和列重构为TSP需要的连通图

在本算法中完成
1、C、R、W的生成
2、CR图的生成。-----FINISHED
5、MAP的生成
3、地图的绘制
4、RX图的生成
"""
def cost(path):
    sum = 0
    for i in range(len(path)):
        sum += maze[path[i][0]][path[i][1]]
    return sum


coordinate = []
i = 0
#   随机在maze上选择n个点作为目的地
while i < C+R:
    a = random.randint(0, row - 1)
    b = random.randint(0, col - 1)
    if ran[a, b] == 0 and maze[a][b] != INF:
        ran[a, b] = -1  # 选过的点就置-1，不再考虑
        coordinate.append([a, b])
        i += 1

customers = copy.deepcopy(coordinate[:C])
restaurants = copy.deepcopy(coordinate[C:])
print(customers)
print(restaurants)
# i = 0
# while i < R:
#     a = random.randint(0, row - 1)
#     b = random.randint(0, col - 1)
#     if ran[a, b] == 0 and maze[a][b] != INF:
#         ran[a, b] = -2  # 选过的点就置-1，不再考虑
#         coordinate.append([a, b])
#         i += 1
print(C+R, "个目的地：", coordinate)
# #   选好了n个节点，接下来开始生成图

graph = np.zeros((C + R, C + R))

edge = [[0 for i in range(col)] for j in range(row)]
#生成CR图
for i in range(0, C + R):
    for j in range(0, C + R):
        #   j轮流抽取候选点
        end_x = coordinate[j][0]
        end_y = coordinate[j][1]
        # MIN = 100000.0
        #   生成代价

        f = []
        if i != j:

            f = _A(coordinate[i][0], coordinate[i][1], end_x, end_y, maze)  # _A会返回一条从j到i的最短路径
            f = copy.deepcopy(list(reversed(f)))  # 存入的是从终点指向起点的路径
            f.append((end_x, end_y))  # 把当前的节点加上
            # print(MIN)
            # print("min road:",m_road)
            # print(f)
            # print(len(f))
            graph[i, j] = cost(f)
            edge[i][j] = f

        else:
            graph[i, j] = -1

        del f
print(graph)
print(edge)

while RUN:
    back = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
    # 搭建基础环境
    _navigation(MAP, BS, back)
    pygame.display.update()
    pygame.time.delay(100)