import pygame
import sys
import numpy as np

# Initialisiere Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Spacegame')

# Colors
BACKGROUND_COLOR = (0, 0, 0)
BODY1_COLOR = (255, 100, 0)
BODY2_COLOR = (255, 200, 100)

# Body 1 settings
body1_radius = 30
body1, body1 = np.array([WIDTH // 2 - 50, HEIGHT // 2]) # // integer division damit keine Pixel gesplittet werden
body1_speed = np.array([0, 0])
body1_acc = np.array([0, 0])

# Body 2 settings
body2_radius = 10
body2 = np.array([WIDTH // 2 + 50, HEIGHT // 2])
body2_speed = np.array([0, 0])
body2_acc = np.array([0, 0])

# Animation loop
clock = pygame.time.Clock()

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # Update body 1 position
    body1_speed += body1_acc
    body1 += body1_speed
    
    # Update body 2 position
    body2_speed += body2_acc
    body2 += body2_speed
    
    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.circle(screen, BODY1_COLOR, body1, body1_radius)
    pygame.draw.circle(screen, BODY2_COLOR, body2, body2_radius)
    
    # Update display
    pygame.display.flip()
    
    # Control the framerate
    clock.tick(60)