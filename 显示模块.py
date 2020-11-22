import  pygame
from 初始化地图 import MAP,STEP,MAPRANK,MAPCROSS,INF,\
                    C,R,W,customers,restaurants,waiter,\
                    CRgraph,CRedge

SIZE_SCREEN = (550, 450)  # 屏幕尺寸
######颜色
QP_C = (200, 200, 200)
BUILD_C = (255, 250, 250)
C_C = (255, 0, 0)
R_C = (50, 250, 250)
#####END
X = 0  # 迷宫起始横坐标
Y = 0  # 迷宫起始纵坐标
BS = min(SIZE_SCREEN)//STEP  # 方格尺寸

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
                                     ((X + e[1] * BS, Y + e[0] * BS), (BS, BS)),
                                     0)
    # 画出顾客
    for c in range(len(customers)):
        screen.blit(pygame.font.Font('freesansbold.ttf',
                                    15).render(f"{c+1}", True, C_C),
                    (X + customers[c][1]* BS + BS // 2, Y + customers[c][0]* BS + BS // 2 ) )
    #画出饭店
    for r in range(len(restaurants)):
        screen.blit(pygame.font.Font('freesansbold.ttf',
                                     20).render(f"{r + 1}", True, R_C),
                    (X + restaurants[r][1] * BS + BS // 2, Y + restaurants[r][0] * BS + BS // 2))

while RUN:
    back = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
    # 搭建基础环境
    _navigation(MAP, BS, back)
    pygame.display.update()
    pygame.time.delay(100)