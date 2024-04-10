import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pool Table")

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

# Function to draw the table
def draw_table():
    # Draw table surface
    pygame.draw.rect(screen, TABLE_COLOR, (100, 100, TABLE_WIDTH, TABLE_HEIGHT))

    # Draw walls
    pygame.draw.rect(screen, WALL_COLOR, (90, 90, WALL_WIDTH, WALL_HEIGHT))
    pygame.draw.rect(screen, WALL_COLOR, (690, 90, WALL_WIDTH, WALL_HEIGHT))
    pygame.draw.rect(screen, WALL_COLOR, (90, 90, TABLE_WIDTH + WALL_WIDTH, WALL_WIDTH))
    pygame.draw.rect(screen, WALL_COLOR, (90, 490, TABLE_WIDTH + WALL_WIDTH, WALL_WIDTH))

    # Draw holes
    hole_radius = BALL_RADIUS * 2
    hole_positions = [(100, 100), (400, 100), (700, 100), (100, 500), (400, 500), (700, 500)]
    for pos in hole_positions:
        pygame.draw.circle(screen, HOLE_COLOR, pos, hole_radius)

# Main loop
running = True
while running:
    screen.fill(WHITE)
    draw_table()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
