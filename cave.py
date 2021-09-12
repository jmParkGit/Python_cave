import sys
from random import randint
import pygame
from pygame.locals import QUIT, Rect, KEYDOWN, K_SPACE

pygame.init()
pygame.key.set_repeat(5,5)

SURFACE_WIDTH=800
SURFACE_HEIGHT=600
CAT_IMAGE_WIDTH=50
CAT_IMAGE_HEIGHT=50
HOLE_HEIGHT_WEIGHT=3
SPEED=1

SURFACE=pygame.display.set_mode((SURFACE_WIDTH,SURFACE_HEIGHT))
FPSCLOCK=pygame.time.Clock()

def main():
    walls=80
    cat_y=100
    velocity=0
    score=0
    slope=randint(1,6)
    sysfont = pygame.font.SysFont(None,36)
    cat_image=pygame.image.load("./data/cat.png")
    cat_image=pygame.transform.scale(cat_image,(CAT_IMAGE_WIDTH,CAT_IMAGE_HEIGHT))
    cloud_image=pygame.image.load("./data/cloud.png")
    holes=[]
    for xpos in range(walls):
        holes.append(Rect(xpos*10, 100, 10, CAT_IMAGE_HEIGHT*HOLE_HEIGHT_WEIGHT))
    game_over=False
    
    while True:
        is_space_down=False
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN:
                if event.key == K_SPACE:
                    is_space_down=True

        if not game_over:
            score+=10

            if is_space_down==True:
                velocity += SPEED*(-1)
            else:
                velocity += SPEED
            cat_y+=velocity
            
            edge=holes[-1].copy()
            test=edge.move(0,slope)
            if test.top<=0 or test.bottom >= SURFACE_HEIGHT:
                slope = randint(1,6) * (-1 if slope>0 else 1)
                edge.inflate_ip(0,-20)
            edge.move_ip(10,slope)
            holes.append(edge)
            del holes[0]
            holes = [x.move(-10,0) for x in holes]

            if holes[0].top>cat_y or holes[0].bottom <cat_y+CAT_IMAGE_HEIGHT:
                game_over=True

        
        SURFACE.fill((0,255,0))
        for hole in holes:
            pygame.draw.rect(SURFACE, (80,188,223), hole)
        SURFACE.blit(cat_image,(0,cat_y))
        score_image=sysfont.render("score is {}".format(score), True, (0,0,225))
        SURFACE.blit(score_image, (600,20))

        if game_over:
            SURFACE.blit(cloud_image, (0,cat_y-40))
            game_over_alarm=sysfont.render("GAME OVER", True, (0,0,225))
            SURFACE.blit(game_over_alarm,(330,250))
        
        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()