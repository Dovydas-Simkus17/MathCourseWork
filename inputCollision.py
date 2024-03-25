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
    def __init__(self,x,y,hitForce,angleHit):
        self.x = x
        self.y = y
        
        self.totalMilliseconds = 0
        self.totalVelocity = []
        self.angleHit = angleHit
        self.hitForce = hitForce

        self.index = 0
        self.moving = True

        self.cueDistance = 0.1
        self.deceleration = (0.03 * 9.8)
        
    def draw(self):
        p.draw.circle(display,(255,255,255),(int(self.x),int(self.y)),10)
        
    def move(self, X, Y, XR, YR):
        self.x += (X * XR)
        self.y += (Y * YR)

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
    
def collsionDetector(balls):
    for ballA in balls:
        for ballB in balls:
            if any(ballA != ballB and (m.sqrt((ballA.x-ballB.x)**2+(ballA.y-ballB.y)**2)<=10+10) for counter in balls):
                print(f"The {get_var_name(ballA)} has collided with {get_var_name(ballB)}")

                ballA.angleHit = ballA.angleHit * (-1)
                ballA.hitForce = (ballA.hitForce + ballB.hitForce) / 1.5
                ballB.hitForce = (ballA.hitForce + ballB.hitForce) / 1.5
                ballA.ballHit()
                movement(ballA)
                ballB.ballHit()
                movement(ballB)
                for i in range(len(balls)):
                    print(balls[i].hitForce)

def inputDetection(balls,user_text,active):
    for ball in balls:
        if all((ball.moving == False and ball1.moving == False) for ball1 in balls):
    
            if active: 
                color = color_active 
            else: 
                color = color_passive 
                
            # draw rectangle and argument passed which should 
            # be on screen 
            p.draw.rect(display, color, input_rect) 
        
            text_surface = font.render(user_text, True, (255, 255, 255)) 
            
            # render at position stated in arguments 
            display.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
            
            # set width of textfield so that text cannot get 
            # outside of user's text input 
            input_rect.w = max(100, text_surface.get_width()+10) 
        
        else:
            display.fill([0,0,0])

    return user_text,active

def get_var_name(var):
    for name, value in globals().items():
        if value is var:
            return name

def movement(ball):
    if(ball.index < ball.totalMilliseconds):
        X,Y,XR,YR = ball.whereBallGo(ball.totalVelocity[ball.index])
        #print("X:" + str(X) + " | Y:" + str(Y) + " | XR:" + str(XR) + " | YR:" + str(YR))
        ball.move(X,Y,XR,YR)
        ball.index += 1
        ball.moving = True
    elif (ball.moving):
        ball.moving = False
        print(f"The {get_var_name(ball)} has Stopped!")

grav = 1
friction = 1

w,h=500,500
display = p.display.set_mode([w,h])
p.display.set_caption("Collision Test")
font = p.font.SysFont("calibri", 20)

x,y=150,150
radius=50
cursorRadius=20
count=0
hit=False
status = True

#fps stuff
fps = 60
clock = p.time.Clock()
forc = 1

#Ball 
ball1 = Ball(200,200, forc, 0)
ball2 = Ball(250,200, 0, 90)
ball3 = Ball(300,200, 0, 90)
balls = [ball1,ball2,ball3]

#ang = int(input(print("Angle to hit?\n")))

ball1.ballHit()
ball2.ballHit()
ball3.ballHit()

#Input Related Variables
input_rect = p.Rect(100, 100, 140, 32)
user_text = ''

#Colour of Text Box
color_active = p.Color('red') 
color_passive = p.Color('blue')
color = color_passive 
active = False

while(status):
    display.fill([0,0,0])
    mx,my=p.mouse.get_pos()

    for event in p.event.get():
        if(event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE)):
            status = False
        if event.type == p.MOUSEBUTTONDOWN: 
                if input_rect.collidepoint(event.pos): 
                    active = True
                else: 
                    active = False

        if event.type == p.KEYDOWN:
            if active:
                if event.key == p.K_RETURN:
                    print(user_text)
                    forc = int(user_text)
                    print(forc)
                    user_text = ''
                    ball1.index = 0
                    ball1.hitForce = forc

                elif event.key == p.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

    user_text, active = inputDetection(balls,user_text,active)
    ball1.ballHit()
    collsionDetector(balls)

    movement(ball1)
    movement(ball2)
    movement(ball3)
    
    ball1.draw()
    ball2.draw()
    ball3.draw()
    


    p.display.update()
    clock.tick(fps)

p.quit()
