#next i want to make it have initial momentum and then begin to arc downwards
import pygame as py
import math as m
import time
# Initialize Pygame
py.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Ball Projectile")
clock = py.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)

#inputs for now
screen.fill(RED)
py.display.flip()
slider_power = 100#int(input("slider_power: "))
slider_angle = m.radians(int(80))#m.radians(int(input("slider_angle (degrees): ")))
tank_x = 30#int(input("tank x: "))
tank_y = 550#int(input("tank y: "))
tank_pos = py.math.Vector2(tank_x, tank_y)

def projectile_motion():
    gravity = py.math.Vector2(0, 20)
    velocity = py.math.Vector2(m.cos(slider_angle) * slider_power , -m.sin(slider_angle) * slider_power)
    position = py.math.Vector2(tank_x, tank_y) 
    running = True
    projectile = True

    prev_time = time.perf_counter()
    while running:

        screen.fill(WHITE) #refills screen as white
        
        #draw static images code here

        current_time = time.perf_counter()
        delta_tp = current_time - prev_time
        prev_time = current_time

        if projectile:
            velocity += gravity * delta_tp * 4 #*4 for increased sim speed
            position += velocity * delta_tp * 4
            print(position)
        # Draw projectile
            py.draw.circle(screen, RED, (int(position.x), int(position.y)), 5)
        # Stop when it goes off the screen
            if position.y > HEIGHT or position.x > WIDTH or position.x < 0:
                projectile = False

        py.display.flip()
        time.sleep(0.01) #limit cpu usage during animation

        for event in py.event.get():
            if event.type == py.QUIT:
                running = False

projectile_motion()



