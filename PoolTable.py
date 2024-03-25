import pygame
import sys
pygame.init()

width,height=950,500
display=pygame.display.set_mode((width, height))
pygame.display.set_caption("8 Ball Pool")

white=(255,255,255)
green=(0,128,0)
brown=(84,43,2)
black=(0,0,0)

ball_radius=15
ball_speed=5
ball_pos=[width//2,height//2]

running = True
while running:
    
    #pool table with borders
    display.fill(green)
    pygame.draw.rect(display,brown,(0,0,width,40))
    pygame.draw.rect(display,brown,(0,0,40,height))
    pygame.draw.rect(display,brown,(width-40,0,width,height))
    pygame.draw.rect(display,brown,(0,height-40,width,height))
    pygame.draw.ellipse(display,black,(width-60,height-60,60,60))
    pygame.draw.ellipse(display,black,(0,0,60,60))
    pygame.draw.ellipse(display,black,(width-60,0,60,60))
    pygame.draw.ellipse(display,black,(0,height-60,60,60))
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    mouse_x,mouse_y=pygame.mouse.get_pos()
    dx=mouse_x-ball_pos[0]
    dy=mouse_y-ball_pos[1]
    distance=max(1,(dx**2+dy**2)**0.5)
    ball_pos[0]+=int(ball_speed*dx/distance)
    ball_pos[1]+=int(ball_speed*dy/distance)

    pygame.draw.circle(display,white,ball_pos,ball_radius)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()