import numpy as np
import pandas as pd
import  pygame
from 初始化地图 import MAP,STEP,MAPRANK,MAPCROSS,INF,\
                    C,R,W,customers,restaurants,waiters,\
                    CRgraph,CRedge,\
                    _A,F
import random
from tsp_with_astar import Solution, tsp
SIZE_SCREEN = (550, 450)  # 屏幕尺寸
######颜色
QP_C = (200, 200, 200)
BUILD_C = (255, 250, 250)
C_C = (255, 0, 0)
R_C = (50, 250, 250)
W_C = (20,30,255)
#####END
X = 0  # 迷宫起始横坐标
Y = 0  # 迷宫起始纵坐标
BS = (min(SIZE_SCREEN)-5)//STEP  # 方格尺寸
#########################################
###背包的安排
bsize = [1,2,5,4,6,1,2,5,4]
bvalue =[3,4,7,3,8,1,2,9,3]
# 显示屏幕初始化
pygame.init()
screen = pygame.display.set_mode(SIZE_SCREEN)
pygame.display.set_caption("外卖模拟系统")
screen.fill(QP_C)
RUN = True


def _navigation(MAP, BS, back):
    # 画地图
    for i in range(MAPRANK):
        for j in range(MAPCROSS):
            if MAP[i][j] == INF:
                    pygame.draw.rect(screen, BUILD_C,
                        ((X + j*BS, Y+ i*BS), (BS, BS)),
                        0)
        # 画出图
    for i in range(C+R):
        for j in range(C+R):
            if CRedge[i][j] != 0:
                for e in CRedge[i][j]:
                    pygame.draw.rect(screen, (255,250, 3),
                                     ((X + e[1] * BS, Y + e[0] * BS), (BS//2, BS//2)),
                                     0)
    # 画出顾客
    for c in range(len(customers)):
        screen.blit(pygame.font.Font('freesansbold.ttf',
                                    20).render(f"{c+1}", True, C_C),
                    (X + customers[c][1]* BS + BS // 2, Y + customers[c][0]* BS + BS // 2 ) )
    #画出饭店
    for r in range(len(restaurants)):
        screen.blit(pygame.font.Font('freesansbold.ttf',
                                     30).render(f"{r + 1}", True, R_C),
                    (X + restaurants[r][1] * BS + BS // 2, Y + restaurants[r][0] * BS + BS // 2))
    #画出外卖员
    for w in range(len(waiters)):
        screen.blit(pygame.font.Font('freesansbold.ttf',
                                     25).render(f"{w + 1}", True, W_C),
                    (X + waiters[w][1] * BS + BS // 2, Y + waiters[w][0] * BS + BS // 2))


def knapsack(things,C):
    n=len(things['s'])+1
    x=list(range(0,C+1))
    y=list(range(0,n))
    a=np.zeros((n, C+1))#放背包
    b=pd.DataFrame(np.zeros((n, C+1)),index=y,columns=x)
    for j in range(1, C + 1):
        for i in range(1,n):
            b.loc[i,j]=b.loc[i-1,j]
            if things['s'][i-1] <=j:
                b.loc[i,j]=max(b.loc[i-1,j],b.loc[i-1,j-things['s'][i-1]]+things['v'][i-1])
                if b.loc[i,j] != b.loc[i-1,j]:
                    a[i][j] = 1
                else:
                    a[i][j] = 0

    reli = []
    i,j =len(things['s']), C
    while i > 0:
        if a[i][j] == 0:
            i -= 1
        else:
            reli.append(i - 1)
            j = j - things['s'][i - 1]
            i -= 1
    return reli,b.loc[n - 1,C]
"""
# order 完成订单操作。
# 订单操作: 选定一些顾客，选择一家餐馆。
生成这个餐馆的订单。
当访问这家餐馆时，应当可以获得包括该餐馆的privateC-R图。
这是大CR图的一个子集，在该图中，餐馆为起始节点
"""
# def order(nbrc,restaurant,)
print("饭店有:",restaurants,"\n顾客有:",customers)
#第一步：下单
ordercustoms = {}
while len(ordercustoms.keys()) < 6:
    k = random.randint(0,C - 1)
    ordercustoms[k] = ordercustoms.get(k,(bsize[k],bvalue[k]//(CRgraph[k][0]*0.02)))

orderlist ={'0':ordercustoms}
print("已收到订单",orderlist)
#第二步：找到外卖员
#给外卖员一个bag
waiterdict = {}
for waiter in waiters:
    waiterdict[waiter] = waiterdict.get(waiter,random.randint(9,12))
print("我们的外卖员:",waiterdict)
for rest in orderlist.keys():
    b = []
    chosedw = [INF,(-1,-1)]
    for waiter in waiterdict.keys():
        waiter = list(waiter)
        md = restaurants[eval(rest)]
        b =  _A(waiter[0],waiter[1],md[0],md[1],MAP)
        if len(b)< chosedw[0]:
            chosedw[0] = len(b)
            chosedw[1] = waiter
    print(rest,"号饭店选择",waiter,"号外卖员工作")
#第三步:外卖员装东西:
    #0-1knapasack
    #初始化
    things = {'s':[],'v':[]}
    for cstm in orderlist[rest].keys():
        things['s'].append( orderlist[rest][cstm][0] )
        things['v'].append( orderlist[rest][cstm][1])
    #装
    waiterchoose,gain = knapsack(things,waiterdict[tuple(chosedw[1])])

    print("外卖员根据DP选择:",waiterchoose,"这几个订单\n他本次的收益是",gain)
    #重构，找出被选中的顾客。
    newnode = [0]
    for cstm in orderlist[rest].keys():
        for k in waiterchoose:
            if orderlist[rest][cstm] == (things['s'][k],things['v'][k]):
                print("下面为这些顾客配送:",customers[cstm])
                newnode.append(cstm + 1)
    newgraph =[]
    for i in range(len(newnode)):
        newgraph.append([])
        for j in range(len(newnode)):
            newgraph[i].append(CRgraph[newnode[i]][newnode[j]])
    newgraph = np.array(newgraph)
    tsp(newgraph, 0, CRedge,newnode)
    #newnode里装着顾客的索引
while RUN:
    back = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
    # 搭建基础环境
    _navigation(MAP, BS, back)
    pygame.display.update()
    pygame.time.delay(100)