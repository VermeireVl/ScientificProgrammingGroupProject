import pygame
import random

pygame.init()

#Display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Tank Game")

#colors
WHITE = (255, 255, 255)
BROWN = (120, 80, 40)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
GREY = (200, 200, 200)

#tank size
TANK_WIDTH = 50
TANK_HEIGHT = 30

clock = pygame.time.Clock()


        
def draw_ground():
    pygame.draw.rect(
        screen,
        BROWN,
        (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
    )



def draw_cloud(x, y):
    # simple 3-circle cloud shape
    pygame.draw.circle(screen, GREY, (x, y), 25)
    pygame.draw.circle(screen, GREY, (x + 30, y + 10), 30)
    pygame.draw.circle(screen, GREY, (x - 25, y + 10), 28)



def draw_tank(x, y, color):
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



def graphics_loop():
    running = True

    #Position of tank in game
    tank1_x = 100
    tank1_y = SCREEN_HEIGHT - GROUND_HEIGHT - TANK_HEIGHT

    tank2_x = 650
    tank2_y = SCREEN_HEIGHT - GROUND_HEIGHT - TANK_HEIGHT

    #make the clouds start at random positions in sky
    cloud_positions = [
        [random.randint(0, SCREEN_WIDTH), random.randint(50, 200)],
        [random.randint(0, SCREEN_WIDTH), random.randint(50, 200)],
        [random.randint(0, SCREEN_WIDTH), random.randint(50, 200)]
    ]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        #Draw clouds and make them move
        for cloud in cloud_positions:
            draw_cloud(cloud[0], cloud[1])
            cloud[0] += 1  #Speed

            #Loop clouds after offscreen
            if cloud[0] > SCREEN_WIDTH + 50:
                cloud[0] = -50
                cloud[1] = random.randint(50, 200)

        #Environment
        draw_ground()
        draw_tank(tank1_x, tank1_y, GREEN)
        draw_tank(tank2_x, tank2_y, BLUE)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()



graphics_loop()
