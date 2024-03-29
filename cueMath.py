#@PydevCodeAnalysisIgnore
#@UndefinedVariable
import pygame as p, sys, random as r, math as m
from pygame.locals import *
from colour import *

p.init()

w,h=500,500
display = p.display.set_mode([w,h])
p.display.set_caption("Collision Test")
font = p.font.SysFont("calibri", 12)

x,y=150,150
radius=50
cursorRadius=20
count=0
hit=False
status = True

#fps stuff
fps = 30
clock = p.time.Clock()

while(status):
    display.fill([0,0,0])
    mx,my=p.mouse.get_pos()

    for event in p.event.get():
        if(event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE)):
            status = False

    p.draw.circle(display,(0,0,255),[x,y],radius,0)

    #Still needs to be fixed
    ### MAIN TEST FOR COLLISION ###
    if(m.sqrt((mx-x)**2+(my-y)**2)<=radius+cursorRadius):
        hit=True
        angle = ((m.atan(((mx%x)-x)**2/(my%y-y)**2)+(180/m.pi)) % 360)*4
        print(angle)
        c1_newpos_x = m.sin(angle) * (radius + cursorRadius) + x
        c1_newpos_y = m.cos(angle) * (radius + cursorRadius) + y
        p.draw.circle(display,(255,255,255),[c1_newpos_x,c1_newpos_y],cursorRadius,0)
    else:
        p.draw.circle(display,(255,255,255),p.mouse.get_pos(),cursorRadius,0)
        hit=False
    xy=font.render(str(p.mouse.get_pos()),True,(255,255,255))
    hitTxt=font.render(str(hit),True,(255,255,255))

    p.draw.line(display,(255,255,255),(0,400),(1000,400),10)

    display.blit(xy,[5,h-15])
    display.blit(hitTxt,[w-30,h-15])

    p.display.update()
    clock.tick(fps)

p.quit()
