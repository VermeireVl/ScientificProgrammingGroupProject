import Cannonball
import pygame

import pygame_gui

# pygame setup
pygame.init()
screenParam = [1280, 720]
screen = pygame.display.set_mode((screenParam[0], screenParam[1]))
ui_manager = pygame_gui.UIManager((screenParam[0], screenParam[1]))
clock = pygame.time.Clock()
CannonballShotDuration = 0

running = True
pos = [0,0]

frameLimit = 60


RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Create a slider
sliderPower = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((screenParam[0] * 0.1, screenParam[1] * 0.9), (screenParam[0] * 0.2, screenParam[1] * 0.025)),
    start_value=5,
    value_range=(0, 100),
    manager = ui_manager
)

sliderAngle = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((screenParam[0] * 0.4, screenParam[1] * 0.9), (screenParam[0] * 0.2, screenParam[1] * 0.025)),
    start_value=50,
    value_range=(0, 180),
    manager = ui_manager
)

button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((screenParam[0] * 0.7, screenParam[1] * 0.9), (screenParam[0] * 0.2, screenParam[1] * 0.05)),
    text="Shoot",
    manager=ui_manager
)

power = float(sliderPower.get_current_value())
angle = float(sliderAngle.get_current_value())

cannonball = Cannonball.Cannonball()


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        ui_manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button:
                cannonball.Shoot(float(sliderAngle.get_current_value()), float(sliderPower.get_current_value()), screenParam[0] * 0.1, screenParam[1] * 0.8)
     # Update the UI
    ui_manager.update(1/frameLimit)  # Delta time (e.g., 1/60 for 60 FPS)
    

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    ui_manager.draw_ui(screen)
    #if pos[0] < screenParam[0] or pos[1] < screenParam[1]:
    #    pos[0] = pos[0] + int(slider.get_current_value())
    #    pos[1] = pos[1] + int(slider.get_current_value())
    #else:
    #    pos[0] = 0
    #    pos[1] = 0



    # RENDER YOUR GAME HERE
    points = [(0,screenParam[1] * 0.3), (screenParam[0], screenParam[1] * 0.3), (screenParam[0], 0), (0,0)]
    #pygame.draw.polygon(screen, (0,0,0), points, 0)

    #currentLocation = Cannonball.calculatePointInArc(angle, power, CannonballShotDuration, screenParam[0] * 0.1, screenParam[1] * 0.8 )

    #if currentLocation[0] > screenParam[0] or currentLocation[1] > screenParam[1] or currentLocation[0] < 0 or currentLocation[1] < 0:
    #    CannonballShotDuration = 0
    #    power = float(sliderPower.get_current_value())
    #    angle = float(sliderAngle.get_current_value())
    #    currentLocation = Cannonball.calculatePointInArc(angle, power, CannonballShotDuration, screenParam[0] * 0.1, screenParam[1] * 0.8 )

    if cannonball.GetActive():
        currentLocation = cannonball.CalculatePointInArc(clock.get_time())
        pygame.draw.circle(screen, (0,0,0), currentLocation, 10)



    

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(frameLimit)  # limits FPS to 60

pygame.quit()