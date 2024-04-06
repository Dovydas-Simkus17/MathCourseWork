import math
import pygame
import pymunk
import pymunk.pygame_util

#Initialising Pygame
pygame.init()

#Window Parameters
windowWidth=1000
windowHeight=600

#Table Parameters
TABLE_WIDTH = 960
TABLE_HEIGHT = 560
WALL_WIDTH = 40
WALL_HEIGHT = 600

#Pool Table Window
window=pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption("8 Ball Pool")

#Creating Pymunk Space
space=pymunk.Space()
friction_body=space.static_body
draw_shapes=pymunk.pygame_util.DrawOptions(window)

#FrameRate Update
frame_update=pygame.time.Clock()
fps=60

#Game Variables
ball_diameter=36
taking_shot=True
force=0
max_force=10000
force_direction=1
power_up=False

#Colors
background=(50,50,50)      #Gray
TABLE_COLOR = (0, 100, 0)  #Green
WALL_COLOR = (139, 69, 19) #Brown
HOLE_COLOR = (0,0,0)       #Black

# Function to draw the table
def draw_table():
    # Draw table surface
    pygame.draw.rect(window, TABLE_COLOR, (20, 20, TABLE_WIDTH, TABLE_HEIGHT))

    # Draw walls
    pygame.draw.rect(window, WALL_COLOR, (0, 0, WALL_WIDTH, WALL_HEIGHT))
    pygame.draw.rect(window, WALL_COLOR, (960, 0, WALL_WIDTH, WALL_HEIGHT))
    pygame.draw.rect(window, WALL_COLOR, (0, 0, TABLE_WIDTH + WALL_WIDTH, WALL_WIDTH))
    pygame.draw.rect(window, WALL_COLOR, (0, 560, TABLE_WIDTH + WALL_WIDTH, WALL_WIDTH))

    # Draw holes
    for pos in hole_positions:
        pygame.draw.circle(window, HOLE_COLOR, pos, hole_radius)

#Hole Information
hole_radius = 30
hole_positions = [(50, 50), (500, 50), (950, 50), (50, 550), (500, 550), (950, 550)]
#Loading Images
cue_ball_image=pygame.image.load("images\cue_ball.png").convert_alpha()
cue_stick_image=pygame.image.load("images\cue_stick.png").convert_alpha()

#Creating A Ball
def create_ball(radius,pos):
    body=pymunk.Body()
    body.position=pos
    shape=pymunk.Circle(body,radius)
    shape.mass=5
    shape.elasticity=0.8
    #Adding Friction
    pivot=pymunk.PivotJoint(friction_body,body,(0,0),(0,0))
    #Disable Correction
    pivot.max_bias=0
    #Emulating Friction
    pivot.max_force=500
    
    space.add(body,shape,pivot)
    return shape

#Cue Ball
pos=(750,windowHeight/2)
cue_ball=create_ball(ball_diameter/2,pos)

#Balls
ball1 = create_ball(ball_diameter/2,(350,300))

ball2 = create_ball(ball_diameter/2,(320,282))
ball3 = create_ball(ball_diameter/2,(320,318))

ball4 = create_ball(ball_diameter/2,(290,264))
ball5 = create_ball(ball_diameter/2,(290,300))
ball6 = create_ball(ball_diameter/2,(290,336))

ball7 = create_ball(ball_diameter/2,(260,246))
ball8 = create_ball(ball_diameter/2,(260,282))
ball9 = create_ball(ball_diameter/2,(260,318))
ball10 = create_ball(ball_diameter/2,(260,354))

ball11 = create_ball(ball_diameter/2,(230,228))
ball12 = create_ball(ball_diameter/2,(230,264))
ball13 = create_ball(ball_diameter/2,(230,300))
ball14 = create_ball(ball_diameter/2,(230,336))
ball15 = create_ball(ball_diameter/2,(230,372))

balls = {ball1,ball2,ball3,ball4,ball5,ball6,ball7,ball8,ball9,ball10,ball11,ball12,ball13,ball14,ball15}


#Create Pool Table Cushions
pool_cushions=[[(60,40),(62,35),(471,40),(469,35)],
               [(528,40),(529,35),(940,40),(938,35)],
               [(40,60),(35,62),(40,541),(35,539)],
               [(965,62),(960,60),(965,539),(960,541)],
               [(62,565),(60,560),(469,565),(471,560)],
               [(531,565),(529,560),(938,565),(940,560)]
               ]

#Creating Cushions
def create_cushion(poly_cushion):
    body=pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position=((0,0))
    shape=pymunk.Poly(body,poly_cushion)
    shape.elasticity=0.8
    space.add(body,shape)
    
for c in pool_cushions:
    create_cushion(c)
    
#Create Cue Stick
class Cue_stick():
    def __init__(self,pos):
        self.original_image=cue_stick_image
        self.angle=0 #Defining the angle
        self.image=pygame.transform.rotate(self.original_image,self.angle)
        self.rect=self.image.get_rect()
        self.rect.center=pos
    
    def update(self,angle):
        self.angle=angle
        
    def draw(self,surface):
        self.image=pygame.transform.rotate(self.original_image,self.angle)
        surface.blit(self.image,
                     (self.rect.centerx-self.image.get_width()/2,
                     self.rect.centery-self.image.get_height()/2))
    
cue_stick=Cue_stick(cue_ball.body.position)

#Game Running Loop
gameRun=True
while gameRun:
    
    frame_update.tick(fps)
    space.step(1/fps)
    
    #Background Color Fill
    window.fill(background)
    
    #Pool Table Draw
    draw_table()
    
    #Cue Ball Draw
    window.blit(cue_ball_image,(cue_ball.body.position[0]-ball_diameter/2,cue_ball.body.position[1]-ball_diameter/2))

    #Balls draw
    for ball in balls:
        window.blit(cue_ball_image,(ball.body.position[0]-ball_diameter/2,ball.body.position[1]-ball_diameter/2))
    
    #Checking If All Balls Have Stopped Moving
    taking_shot=True
    if int(cue_ball.body.velocity[0])!=0 or int(cue_ball.body.velocity[1])!=0:
        taking_shot=False
    
    #Cue Stick Draw / Calculating The Cue Stick Angle
    if taking_shot==True:
        mouse_pos=pygame.mouse.get_pos()
        cue_stick.rect.center=cue_ball.body.position
        x_distance=cue_ball.body.position[0]-mouse_pos[0]
        #Y is negative as pygame y coordinates increase down the screen
        y_distance=-(cue_ball.body.position[1]-mouse_pos[1])
        cue_stick_angle=math.degrees(math.atan2(y_distance,x_distance))
        cue_stick.update(cue_stick_angle)
        cue_stick.draw(window)
    
    #Power Up Code
    if power_up==True:
        force+=100*force_direction
        if force>=max_force or force<=0:
            force_direction*=-1
        print(force)
    elif power_up==False and taking_shot==True:
        x_impulse=math.cos(math.radians(cue_stick_angle))
        y_impulse=math.sin(math.radians(cue_stick_angle))
        cue_ball.body.apply_impulse_at_local_point((force*-x_impulse,force*y_impulse))
        force=0
    #Pots
    for ball in balls:
        ballRemove = False
        ballPos = ball.body.position
        for pos in hole_positions:
            if any((math.sqrt((ballPos[0]-pos[0])**2+(ballPos[1]-pos[1])**2)<=ball_diameter) for counter in balls):
                balls.remove(ball)
                ballRemove = True
        if ballRemove == True:
            break
            
    #Event Handler
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN and taking_shot==True:
            power_up=True
        
        if event.type==pygame.MOUSEBUTTONUP and taking_shot==True:
            power_up=False
            
        if event.type==pygame.QUIT:
            gameRun=False
                 
    #space.debug_draw(draw_shapes) Code That Visualised The Cue Ball Shape And Boundaries
    pygame.display.update()
            
pygame.quit()
