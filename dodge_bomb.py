import os
import sys
import random
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {  #移動量辞書、(押下キー:移動量タプル)
    pg.K_UP: (0,-5),
    pg.K_DOWN : (0, +5),
    pg.K_LEFT : (-5,0),
    pg.K_RIGHT : (+5,0),
}



os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect,または,爆弾Rectの画面内外判定用の関数
    引数:こうかとんRect,または,爆弾Rect
    戻り値:横方向判定結果、縦方向判定結果(True:画面内/False:画面外)
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate 


def time():
    new_lst = []
    accs = [a for a in range(1,11)]

    for r in range(1,11):
        bb_img = pg.Surface((20*r,20*r))
        bb_img.set_colorkey((0,0,0))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        new_lst.append(bb_img)
    return accs , new_lst
    
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # ここからこうかとんの設定
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    # ここから爆弾の設定
    accs, new_lst = time()
    bb_img = new_lst[0]
    bd_rct = bb_img.get_rect()
    bd_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy = +5,+5 #横方向速度,縦方向速度

    clock = pg.time.Clock()
    tmr = 0
 
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bd_rct):
            print("Game Over")
            return
        screen.blit(bg_img, [0, 0]) 
        #こうかとんの移動と表示
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        #爆弾の移動と表示 avx = vx * accs[min(tmr//500, 9)]
        avx = vx * accs[min(tmr//500, 9)]
        avy = vy * accs[min(tmr//500, 9)]
        bd_rct.move_ip(avx,avy)
        bb_img = new_lst[min(tmr//500, 9)]
        screen.blit(bb_img,bd_rct)
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
