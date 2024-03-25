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
        self.mass = 0.05

        self.index = 0
        self.moving = True

        self.cueDistance = 0.1
        self.deceleration = (0.03 * 9.8)
    
    def getX(self):
        return (self.x)
    def getY(self):
        return (self.y)

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
    def velocityCreation(self):
        #Calculation for the velocity of a ball
        velocity = m.sqrt((2 * self.hitForce * self.cueDistance)/self.mass)
        return (velocity)
    def ballHit(self,velocity):
        #Calculate distance ball has travelled
        distance = (velocity**2) / (2 * self.deceleration)
        #Calculates time
        time = m.sqrt((2*distance)/self.deceleration)

        milliseconds = np.arange(0,time,0.1)
        self.totalMilliseconds = self.totalMilliseconds + len(milliseconds)
        i = 0 + self.index
        self.totalVelocity = [velocity-(velocity*((i+1)/self.totalMilliseconds)) for i in range(self.totalMilliseconds)]

    """ def wow1(self, ball2):
        v = (2 * 0.05)/(0.05 + 0.05) * ball2.totalVelocity[ball2.index-1]
        self.wow2(v)
    
    def wow2(self, velocity):
        #Calculate distance ball has travelled
        distance = (velocity**2) / (2 * self.deceleration)
        #Calculates time
        time = m.sqrt((2*distance)/self.deceleration)

        milliseconds = np.arange(0,time,0.1)
        self.totalMilliseconds = len(milliseconds)
        self.totalVelocity = [velocity-(velocity*((i+1)/self.totalMilliseconds)) for i in range(self.totalMilliseconds)]
        self.index = 2 """

def phiAngle(ballI,ballII):
    #temp
    """ x1 = ballI.getX()
    x2 = ballII.getX()
    y1 = ballI.getY()
    y2 = ballII.getY()

    print (y1)
    print (y2)
    print (x2)
    print (x1)

    x = abs(x2 - x1)
    y = abs(y2 - y1)

    print(x)
    print(y)

    h = m.sqrt(x*x - y*y)

    print(h)



    angle = m.acos((y/h)) """

    return (270)

def wow1(ballI, ballII,index):

    m1 = ballI.mass
    m2 = ballII.mass
    v1 = ballI.totalVelocity[ballI.index-1] 
    v2 = ballII.totalVelocity[ballII.index-1]
    angle1 = ballI.angleHit
    angle2 = ballII.angleHit
    phi = phiAngle(ballI,ballII)
    equation1 = ((((v1 * m.cos(angle1 - phi)) * (m1-m2)) + (2*m2*v2 * m.cos(angle2 - phi)))/(m1+m2))
    if index == 0:
        finalequation = (equation1*m.cos(phi)) + v1*m.sin(angle1 - phi) * m.cos(phi + m.pi/2)
    else:
        finalequation = (equation1*m.sin(phi)) + v1*m.sin(angle1 - phi) * m.sin(phi + m.pi/2)
    ballI.ballHit(finalequation)
    

        
    
def get_var_name(var):
    for name, value in globals().items():
        if value is var:
            return name






        
cool = 0
    

    
def collsionDetector(balls,cool):
    ballAra = ["",""]
    for ball in balls:
        if any(ball != ball1 and (m.sqrt((ball.x-ball1.x)**2+(ball.y-ball1.y)**2)<=10+10) for ball1 in balls):
            print("COLLISION DETECTION")
            print(get_var_name(ball))
            if (ballAra[0] != ""):
                    ballAra[1] = ball
                    wow1(ballAra[0],ballAra[1],0)
                    wow1(ballAra[1],ballAra[0],1)
            ballAra[0] = ball


    """ ballAra = ["",""]
    for ballA in balls:
        for ballB in balls:
            if any(ballA != ballB and (m.sqrt((ballA.x-ballB.x)**2+(ballA.y-ballB.y)**2)<=10+10) for counter in balls):
                print(f"The {get_var_name(ballA)} has collided with {get_var_name(ballB)}")
                
                ballAra[0] = ballA
                if (ballAra[0] != ""):
                    ballAra[1] = ball

                    ballAra[0].wow1(ballAra[1],0)
                    ballAra[1].wow1(ballAra[0],1) """
        

            
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
    elif (ball.moving):
        ball.moving = False
        print(f"The {get_var_name(ball)} has Stopped!")


cool = 0

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
fps = 10
clock = p.time.Clock()

#Ball 
ball1 = Ball(200,210, 4, 270)
ball2 = Ball(250,230, 4, 270)
ball3 = Ball(300,210, 4, 90)
balls = {ball1,ball2,ball3}

""" ang = int(input(print("Angle to hit?\n")))
forc = int(input(print("Force to hit?\n"))) """

for ball in balls:
    ball.ballHit(ball.velocityCreation())




while(status):
    display.fill([0,0,0])
    mx,my=p.mouse.get_pos()

    for event in p.event.get():
        if(event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE)):
            status = False
    
    collsionDetector(balls,cool)

    movement(ball1)
    movement(ball2)
    movement(ball3)
    
    ball1.draw()
    ball2.draw()
    ball3.draw()
    
    p.display.update()
    clock.tick(fps)

p.quit()
