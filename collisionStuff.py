#@PydevCodeAnalysisIgnore
#@UndefinedVariable
import pygame as p, sys, random as r, math as m
from pygame.locals import *
from colour import *
import numpy as np

p.init()

#Triangles that calculate the change of X and Y coordinate
#with one side and one angle
def triangleX(v,theta):
    X = v * m.sin(theta)
    Y = v * m.cos(theta)
    return(X,Y)

def triangleY(v,theta):
    X = v * m.cos(theta)
    Y = v * m.sin(theta)
    return(X,Y)    

class Ball():
    def __init__(self):
        self.x = 200
        self.y = 200
        
        self.totalMilliseconds = 0
        self.totalVelocity = []
        self.angleHit = angleHit
        self.hitForce = hitForce

        self.moving = True

        self.cueDistance = 0.1
        self.deceleration = (0.03 * 9.8)
        
    def draw(self):
        p.draw.circle(display,(255,255,255),(int(self.x),int(self.y)),10)
        
    def move(self, X, Y, XR, YR):
        self.y += (X * XR)
        self.x += (Y * YR)

    def whereBallGo(self,v):
        #Changes where ball goes according to angle
        self.angleHit = self.angleHit % 360
        hitX = 0
        hitY = 0
        rangeX = -1
        rangeY = -1
        
        if self.angleHit > 270:
            hitX, hitY = triangleX(v,((self.angleHit)%90))
            rangeX = 1
            rangeY = 1
            #-x,y
        elif self.angleHit == 270:
            hitX = v
            rangeX = 1
            #x,y
        elif self.angleHit > 180:
            hitX, hitY = triangleY(v,((self.angleHit)%90))
            rangeX = 1
            #x,y
        elif self.angleHit == 180:
            hitY = v
            #x,y
        elif self.angleHit > 90:
            hitX, hitY = triangleX(v,((self.angleHit)%90))
            #-x,y
        elif self.angleHit == 90:
            hitX = v
            #-x,y
        elif self.angleHit > 0:
            hitX, hitY = triangleY(v,((self.angleHit)%90))
            rangeY = 1
            #-x,-y
        else:
            hitY = v
            rangeY = 1
            #x,-y
        return (hitX,hitY,rangeX,rangeY)
        
    def ballHit(self):
        #Calculation for the velocity of a ball
        velocity = m.sqrt((2 * self.hitForce * self.cueDistance)/0.05)
        #Calculate distance ball has travelled
        distance = (velocity**2) / (2 * self.deceleration)
        #Calculates time
        time = m.sqrt((2*distance)/self.deceleration)

        milliseconds = np.arange(0,time,0.1)
        self.totalMilliseconds = len(milliseconds)
        self.totalVelocity = [velocity-(velocity*((i+1)/self.totalMilliseconds)) for i in range(self.totalMilliseconds)]
    

grav = 1
friction = 1

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
fps = 60
clock = p.time.Clock()

#Ball 
ball1 = Ball(200,200, 3, 270)
ball2 = Ball(250,200, 3, 90)
ball3 = Ball(300,200, 4, 90)
i=0
j=0
k=0

""" ang = int(input(print("Angle to hit?\n")))
forc = int(input(print("Force to hit?\n"))) """
ball1.ballHit()
ball2.ballHit()
ball3.ballHit()


while(status):
    display.fill([0,0,0])
    mx,my=p.mouse.get_pos()

    for event in p.event.get():
        if(event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE)):
            status = False
    
    """ p.draw.circle(display,(0,0,255),[x,y],radius,0)

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
    display.blit(hitTxt,[w-30,h-15]) """

    if(i < ball1.totalMilliseconds):
        X,Y,XR,YR = ball1.whereBallGo(ball1.totalVelocity[i])
        #print("X:" + str(X) + " | Y:" + str(Y) + " | XR:" + str(XR) + " | YR:" + str(YR))
        ball1.move(X,Y,XR,YR)
        i += 1
    elif (ball1.moving):
        ball1.moving = False
        print("Ball1 Stopped!")

    if(j < ball2.totalMilliseconds):
        X,Y,XR,YR = ball2.whereBallGo(ball2.totalVelocity[j])
        #print("X:" + str(X) + " | Y:" + str(Y) + " | XR:" + str(XR) + " | YR:" + str(YR))
        ball2.move(X,Y,XR,YR)
        j += 1
    elif (ball2.moving):
        ball2.moving = False
        print("Ball2 Stopped!")


    if(k < ball3.totalMilliseconds):
        X,Y,XR,YR = ball3.whereBallGo(ball3.totalVelocity[k])
        #print("X:" + str(X) + " | Y:" + str(Y) + " | XR:" + str(XR) + " | YR:" + str(YR)
        ball3.move(X,Y,XR,YR)
        k += 1
    elif (ball3.moving):
        ball3.moving = False
        print("Ball3 Stopped!")
    
    ball1.draw()
    ball2.draw()
    ball3.draw()
    
    p.display.update()
    clock.tick(fps)

p.quit()
