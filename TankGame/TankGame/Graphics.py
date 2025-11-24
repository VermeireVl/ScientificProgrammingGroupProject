import pygame
#colors
WHITE = (255, 255, 255)
BROWN = (120, 80, 40)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
GREY = (200, 200, 200)

#tank size
TANK_WIDTH = 50
TANK_HEIGHT = 20




def draw_cloud(x, y, screen):
    # simple 3-circle cloud shape
    pygame.draw.circle(screen, WHITE, (x, y), 25)
    pygame.draw.circle(screen, WHITE, (x + 30, y + 10), 30)
    pygame.draw.circle(screen, WHITE, (x - 25, y + 10), 28)



def draw_tank(x, y, color, screen):
    #Tank body
    pygame.draw.rect(screen, color, (x, y, TANK_WIDTH, TANK_HEIGHT))

    #Turret
    turret_x = x + TANK_WIDTH // 2 - 10
    turret_y = y - 10
    pygame.draw.rect(screen, color, (turret_x, turret_y, 20, 10))

    #Barrel
    barrel_start = (turret_x + 10, turret_y)
    barrel_end = (turret_x + 10, turret_y - 25)
    pygame.draw.line(screen, color, barrel_start, barrel_end, 5)
