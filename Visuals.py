import pygame as pg
import math
pg.init()
#Background
X = 600
Y = 600

scrn = pg.display.set_mode((X,Y))

pg.display.set_caption('Moving Stuff')

imp = pg.image.load("H:\\23_24\\Second_Semester\\Web Dev\\CourseWork\\IMAGES\\logo.png")
scrn.blit(imp,(0,0))

#For object in the game
x = 200
y = 500

width = 50
height = 50

vel = 10

x1=100
gravity = 5
# Creating a new rect for first object
player_rect = pg.Rect(10, 20, 50, 50)
 
# Creating a new rect for second object
player_rect2 = pg.Rect(10, 0, 50, 50)

#fps stuff
fps = 30
clock = pg.time.Clock()

#Run the program
status = True
while (status):

    # Program can close
    for i in pg.event.get():
        if i.type == pg.QUIT:
            status = False
    
    player_rect2.bottom += gravity

    collide = pg.Rect.colliderect(player_rect,player_rect2)

    if collide:
        player_rect2.bottom = player_rect.top

    keys = pg.key.get_pressed()

    if keys[pg.K_a] and player_rect.x>0:

        player_rect.x -= vel
    if keys[pg.K_d] and player_rect.x<600-width:

        player_rect.x += vel
    if keys[pg.K_s] and player_rect.y<600-height:

        player_rect.y += vel
    if keys[pg.K_w] and player_rect.y>0:

        player_rect.y -= vel

    scrn.fill((0,0,0))
    
    pg.draw.rect(scrn, (255,0,0), player_rect)
    pg.draw.rect(scrn, (0,255,0), player_rect2)
    pg.draw.circle(scrn,(0,0,255),(x1,200),5)

    pg.draw.circle(scrn,(0,0,255),(500,200),5)

    pg.display.update()
    clock.tick(fps)

pg.quit()