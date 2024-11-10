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
body1_mass = 10e2
body1= np.array([WIDTH // 2 - 50, HEIGHT // 2], dtype=float) # // integer division damit keine Pixel gesplittet werden
body1_speed = np.array([0, 3], dtype=float)
body1_acc = np.array([0, 0], dtype=float)

# Body 2 settings
body2_radius = 10
body2_mass = 10e2
body2 = np.array([WIDTH // 2 + 50, HEIGHT // 2], dtype=float)
body2_speed = np.array([0, -2], dtype=float)
body2_acc = np.array([0, 0], dtype=float)

# Kamera-Startposition
camera_position = np.array([WIDTH // 2, HEIGHT // 2], dtype=float)

# Constants
G = 70e-2

# Animation loop
clock = pygame.time.Clock()

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    distance_b1b2 = np.linalg.norm(body2 - body1)
    if distance_b1b2 < 1:
        distance_b1b2 = 1
    
    # Beschleunigungen berechnen
    body1_acc = (G * body2_mass * (body2 - body1))/(distance_b1b2**3)
    body2_acc = (G * body1_mass * (body1 - body2))/(distance_b1b2**3)
    
    # Update body 1 position
    body1_speed += body1_acc
    body1 += body1_speed
    
    # Update body 2 position
    body2_speed += body2_acc
    body2 += body2_speed
    
    # Kamera folgt den Körpern, wenn sie nahe an die Bildschirmränder kommen
    if body1[0] < camera_position[0] - WIDTH // 4:
        camera_position[0] = body1[0] + WIDTH // 4
    elif body1[0] > camera_position[0] + WIDTH // 4:
        camera_position[0] = body1[0] - WIDTH // 4
    if body1[1] < camera_position[1] - HEIGHT // 4:
        camera_position[1] = body1[1] + HEIGHT // 4
    elif body1[1] > camera_position[1] + HEIGHT // 4:
        camera_position[1] = body1[1] - HEIGHT // 4
    
    # Berechne die relativen Positionen zur Kamera
    body1_screen_pos = body1 - camera_position + np.array([WIDTH // 2, HEIGHT // 2])
    body2_screen_pos = body2 - camera_position + np.array([WIDTH // 2, HEIGHT // 2])

    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.circle(screen, BODY1_COLOR, body1_screen_pos.astype(int), body1_radius)
    pygame.draw.circle(screen, BODY2_COLOR, body2_screen_pos.astype(int), body2_radius)
    
    # Update display
    pygame.display.flip()
    
    # Control the framerate
    clock.tick(60)