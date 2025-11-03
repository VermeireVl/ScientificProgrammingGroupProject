import Cannonball
import pygame

import pygame_gui

# pygame setup
pygame.init()
screenParam = [1280, 720]
screen = pygame.display.set_mode((screenParam[0], screenParam[1]))
ui_manager = pygame_gui.UIManager((screenParam[0], screenParam[1]))
clock = pygame.time.Clock()

running = True
pos = [0,0]

frameLimit = 60


RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Create a slider
sliderPower = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((screenParam[0] * 0.1, screenParam[1] * 0.9625), (screenParam[0] * 0.2, screenParam[1] * 0.025)),
    start_value=10,
    value_range=(0, 100),
    manager = ui_manager
)

sliderAngle = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((screenParam[0] * 0.4, screenParam[1] * 0.9625), (screenParam[0] * 0.2, screenParam[1] * 0.025)),
    start_value=50,
    value_range=(0, 180),
    manager = ui_manager
)

button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((screenParam[0] * 0.7, screenParam[1] * 0.95), (screenParam[0] * 0.2, screenParam[1] * 0.05)),
    text="Shoot",
    manager=ui_manager
)
levelGeometry = [(0,screenParam[1] * 0.8), (screenParam[0] * 0.3, screenParam[1] * 0.8),
                     (screenParam[0]* 0.5, screenParam[1] * 0.85), (screenParam[0]* 0.8, screenParam[1] * 0.75),
                     (screenParam[0], screenParam[1] * 0.75), (screenParam[0],screenParam[1] * 0.95),
                     (0,screenParam[1] * 0.95)]

cannonball = Cannonball.Cannonball(levelGeometry, 5)

tankDetails = [screenParam[0] * 0.1, screenParam[1] * 0.79, 20, 20]


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        ui_manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button:
                cannonball.Shoot(float(sliderAngle.get_current_value()), float(sliderPower.get_current_value()), tankDetails[0], tankDetails[1])
     # Update the UI
    ui_manager.update(1/frameLimit)  # Delta time (e.g., 1/60 for 60 FPS)
    

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    



    # RENDER YOUR GAME HERE
    
    

    pygame.draw.polygon(screen, (0,60,128), levelGeometry, 0)

    pygame.draw.rect(screen, (0,0,0), (tankDetails[0], tankDetails[1], tankDetails[2],tankDetails[3]))
    
    if cannonball.GetActive():
        currentLocation = cannonball.CalculatePointInArc(clock.get_time())
        pygame.draw.circle(screen, (128,75,0), currentLocation, cannonball.GetRadius())

    #Draw UI stuff
    points = [(0,screenParam[1] * 0.95), (screenParam[0], screenParam[1] * 0.95), (screenParam[0], screenParam[1]), (0,screenParam[1])]
    pygame.draw.polygon(screen, (0,0,0), points, 0)
    ui_manager.draw_ui(screen)

    

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(frameLimit)  # limits FPS to 60

pygame.quit()