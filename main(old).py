#@PydevCodeAnalysisIgnore
#@UndefinedVariable
import pygame as p, sys, random as r, math as m
from pygame.locals import *
from colour import *
import numpy as np
import math as m

p.init()


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define constants
BALL_RADIUS = 10
TABLE_COLOR = (0, 100, 0)  # Green
WALL_COLOR = (139, 69, 19)  # Brown
HOLE_COLOR = BLACK
TABLE_WIDTH = 600
TABLE_HEIGHT = 400
WALL_WIDTH = 20
WALL_HEIGHT = 400



# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Pool Table")


status = True

#fps stuff
fps = 10
clock = p.time.Clock()



class Ball():
    def __init__(self,x,y,forc,ang):

        self.x = x
        self.y = y

        self.velocityX = []
        self.velocityY = []

        self.angle = ang

        self.hitForce = forc
        self.cueDistance = 1
        self.mass = 0.05

        self.totalMilliseconds = 0
        self.totalVelocity = []
        self.index = 0

        self.moving = True


    def move(self):

        self.x += self.velocityX[self.index]
        self.y += self.velocityY[self.index]
        
        #self.x = self.x + self.velocity*m.cos(m.radians(self.angle))
        #self.y = self.y + self.velocity*m.sin(m.radians(self.angle))
        
    def draw(self):
        p.draw.circle(screen,(255,255,255),(int(self.x),int(self.y)),10)


    def initialVelocity(self):
        #Calculation for the velocity of a ball
        velocity = m.sqrt((2 * self.hitForce * self.cueDistance)/self.mass)
        print(velocity)
        velocityX = velocity * m.cos(m.radians(self.angle))
        velocityY = velocity * m.sin(m.radians(self.angle))

        return (velocityX, velocityY)

    def ballHit(self, velocityX,velocityY):

        velocity = m.sqrt(velocityX**2 + velocityY**2)

        acceleration = -(0.03 * 9.8)

        #print(velocity)
        #print(acceleration)

        time = (0 - velocity) / acceleration

        #print(time)
        
        
        milliseconds = np.arange(0,time,0.1)
        #print(milliseconds)
        self.totalMilliseconds = self.totalMilliseconds + len(milliseconds)
        #print(self.totalMilliseconds)

        i = 0 + self.index
        self.totalVelocity = [velocity-(velocity*((i+1)/self.totalMilliseconds)) for i in range(self.totalMilliseconds)]
        self.velocityX = [velocityX-(velocityX*((i+1)/self.totalMilliseconds)) for i in range(self.totalMilliseconds)]
        self.velocityY = [velocityY-(velocityY*((i+1)/self.totalMilliseconds)) for i in range(self.totalMilliseconds)]
        #print(self.velocityX)
        #print(self.velocityY)
        if self.totalVelocity == []:
            self.totalVelocity = [0]
        if self.velocityX == []:
            self.velocityX = [0]
        if self.velocityY == []:
            self.velocityY = [0]



def get_var_name(var):
    for name, value in globals().items():
        if value is var:
            return name

# Function to draw the table
def draw_table():
    # Draw table surface
    p.draw.rect(screen, TABLE_COLOR, (100, 100, TABLE_WIDTH, TABLE_HEIGHT))

    # Draw walls
    p.draw.rect(screen, WALL_COLOR, (90, 90, WALL_WIDTH, WALL_HEIGHT))
    p.draw.rect(screen, WALL_COLOR, (690, 90, WALL_WIDTH, WALL_HEIGHT))
    p.draw.rect(screen, WALL_COLOR, (90, 90, TABLE_WIDTH + WALL_WIDTH, WALL_WIDTH))
    p.draw.rect(screen, WALL_COLOR, (90, 490, TABLE_WIDTH + WALL_WIDTH, WALL_WIDTH))

    # Draw holes
    hole_radius = BALL_RADIUS * 2
    hole_positions = [(115, 115), (400, 115), (685, 115), (115, 485), (400, 485), (685, 485)]
    for pos in hole_positions:
        p.draw.circle(screen, HOLE_COLOR, pos, hole_radius)



def nextMovement(ball):

    nextX = ball.x + ball.velocityX[ball.index] 
    nextY = ball.y + ball.velocityY[ball.index]
    
    return(nextX,nextY)


def collisionDetector(balls):
    for ballB in balls:
        for ballA in balls:
            if (ballA != ballB):
                xA, yA = nextMovement(ballB)
                xB, yB = nextMovement(ballA)
                if any((m.sqrt((xA-xB)**2+(yA-yB)**2)<=10+10) for counter in balls):
                    print(f"The {get_var_name(ballA)} has collided with {get_var_name(ballB)}")

                    x1 = ballB.x
                    x2 = ballA.x

                    y1 = ballB.y
                    y2 = ballA.y


                    v1 = np.array([ballB.totalVelocity[ballB.index] * m.cos(m.radians(ballB.angle)), ballB.totalVelocity[ballB.index] * m.sin(m.radians(ballB.angle))])
                    v2 = np.array([ballA.totalVelocity[ballA.index] * m.cos(m.radians(ballA.angle)), ballA.totalVelocity[ballA.index] * m.sin(m.radians(ballA.angle))])

                    MFv1,MFv2 = ballCollision(x1,x2,y1,y2,v1,v2)

                    ballB.angle = findAngle(MFv1)
                    ballA.angle = findAngle(MFv2)

                    #ballB.ballHit(10,10)
                    ballB.ballHit(MFv1[0],MFv1[1])
                    ballA.ballHit(MFv2[0],MFv2[1])


                    #print(MFv1, MFv2)


def findAngle(velocity):
    x = velocity[0]
    y = velocity[1]

    v = m.sqrt(x**2 + y**2)

    if x==0:
        x=0.01
    if y==0:
        y=0.01
    
    position = 0
    if x > 0 and y > 0:
        position = 0
    elif x > 0 and y < 0:
        position = 270
    elif x < 0 and y > 0:
        position = 90
    elif x < 0 and y < 0:
        position = 180
        
    angle = position + ( m.asin(abs(y) / v))
    #print(angle)
    return (angle)


                    


def ballCollision(x1,x2,y1,y2,v1,v2):

    n = np.array([x2-x1,y2-y1])
    #print(n)

    un = (n)/m.sqrt(n[0]**2+n[1]**2)
    #print(un)

    ut = [-un[1],un[0]]
    #print(ut)


    v1n = un*v1
    v1t = ut*v1
    v2n = un*v2
    v2t = ut*v2

    Fv1t = v1
    Fv2t = v2

    Fv1n = (v1n*(0.05-0.05)+2*0.05*v2n)/0.05+0.05
    Fv2n = (v2n*(0.05-0.05) + 2*0.05*v1n)/0.05+0.05

    MFv1n = Fv1n * un
    MFv1t = Fv1t * ut
    MFv2n = Fv2n * un
    MFv2t = Fv1t * un

    MFv1 = MFv1n + MFv1t
    MFv2 = MFv2n + MFv2t

    return (MFv1,MFv2)




def movement(ball):
    if(ball.index < ball.totalMilliseconds):       
        ball.move()

        if (ball.index < len(ball.totalVelocity)-1):
            ball.index += 1
        else:
            ball.index = ball.index
        ball.moving = True
    elif (ball.moving):
        ball.moving = False
        print(f"The {get_var_name(ball)} has Stopped!")





#Ball 
ball1 = Ball(250,305,10,0)
ball2 = Ball(500,300,0,0)
ball3 = Ball(530,285.5,0,0)
ball4 = Ball(530,312.5,0,0)
ball5 = Ball(560,272.5,0,0)
ball6 = Ball(560,300,0,0)
ball7 = Ball(560,327.5,0,0)
balls = {ball1,ball2,ball3,ball4,ball5,ball6,ball7}

for ball in balls:
    X, Y = ball.initialVelocity()
    ball.ballHit(X,Y)

while(status):
    screen.fill(WHITE)
    draw_table()

    for event in p.event.get():
        if(event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE)):
            status = False
                


    for ball in balls:
        ball.draw()
    
    
    for ball in balls:
        movement(ball)

    collisionDetector(balls)


    p.display.update()
    clock.tick(fps)

p.quit()
