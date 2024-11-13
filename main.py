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
# BODY1_COLOR = (255, 100, 0)
# BODY2_COLOR = (255, 200, 100)
BODY_COLOR = np.array([[0, 0, 255], [255, 100, 0], [255, 200, 100]])

body_radius = np.array([3, 30, 10])
body_mass = np.array([10e-5, 10e3, 5e3])
body = np.zeros((3, 2), dtype=float)
body_speed = np.zeros((3, 2), dtype=float)
body_acc = np.zeros((3, 2), dtype=float)

# Body 0 Anfangsbedingungen                 # Player
body[0] = np.array([WIDTH // 2, HEIGHT // 2])
body_speed[0] = np.array([0, 1])
body_acc[0] = np.array([0, 0])

# Body 1 Anfangsbedingungen                 # Stern
body[1] = np.array([WIDTH // 2 - 100, HEIGHT // 2])
body_speed[1] = np.array([0, 2])
body_acc[1] = np.array([0, 0])

# Body 2 Anfangsbedingungen                 # Planet
body[2] = np.array([WIDTH // 2 + 70, HEIGHT // 2])
body_speed[2] = np.array([0, 0])
body_acc[2] = np.array([0, 0])

# # Body 1 settings
# body1_radius = 30
# body1_mass = 10e2
# body1= np.array([WIDTH // 2 - 50, HEIGHT // 2], dtype=float) # // integer division damit keine Pixel gesplittet werden
# body1_speed = np.array([0, 3], dtype=float)
# body1_acc = np.array([0, 0], dtype=float)

# # Body 2 settings
# body2_radius = 10
# body2_mass = 10e2
# body2 = np.array([WIDTH // 2 + 50, HEIGHT // 2], dtype=float)
# body2_speed = np.array([0, -2], dtype=float)
# body2_acc = np.array([0, 0], dtype=float)

# Constants
G = 30e-3

# Glättung der Kamera: Startposition
camera_position = body[0].copy()

# Animation loop
clock = pygame.time.Clock()

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    body_acc[:] = 0                         # Beschleunigungen in jedem Frame resetten, sonst System instabil
    
    for i in range(len(body)):              # Berechnung der Beschleunigung
        for j in range(len(body)):
            if i != j:
                direction = body[j] - body[i]   # Richtung der Kraftquelle  
                distance = np.linalg.norm(direction)
                if distance < 1:
                    distance = 1            # Vermeidung von Singularitäten
                body_acc[i] += (G * body_mass[j] * direction) / (distance**3)
    
    for i in range(len(body)):              # Berechnung von Geschwindigkeit und Position
        body_speed[i] += body_acc[i]
        body[i] += body_speed[i]
    
    # Kameraposition glätten
    alpha = 0.3  # Glättungsfaktor (0.1 = stark geglättet, 0.5 = weniger geglättet)
    camera_position += alpha * (body[0] - camera_position)
    
    # Offset basierend auf der Position von Body 0
    offset = np.array([WIDTH // 2, HEIGHT // 2]) - body[0]

    
    # distance_b1b2 = np.linalg.norm(body2 - body1)
    # if distance_b1b2 < 1:
    #     distance_b1b2 = 1
    
    # # Beschleunigungen berechnen
    # body1_acc = (G * body2_mass * (body2 - body1))/(distance_b1b2**3)
    # body2_acc = (G * body1_mass * (body1 - body2))/(distance_b1b2**3)
    
    # # Update body 1 position
    # body1_speed += body1_acc
    # body1 += body1_speed
    
    # # Update body 2 position
    # body2_speed += body2_acc
    # body2 += body2_speed

    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    
    for i in range(len(body)):
        # Transformiere die Position relativ zu Body 0
        transformed_position = body[i] + offset
        pygame.draw.circle(screen, BODY_COLOR[i], transformed_position.astype(int), body_radius[i])
    
    # pygame.draw.circle(screen, BODY1_COLOR, body1.astype(int), body1_radius)
    # pygame.draw.circle(screen, BODY2_COLOR, body2.astype(int), body2_radius)
    
    # Update display
    pygame.display.flip()
    
    # Control the framerate
    clock.tick(60)