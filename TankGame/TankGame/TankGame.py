import Cannonball
import Tank
import DataAnalysis
import pygame

import pygame_gui

# pygame setup
pygame.init()
screenParam = [1280, 720]
screen = pygame.display.set_mode((screenParam[0], screenParam[1]))
ui_manager = pygame_gui.UIManager((screenParam[0], screenParam[1]))
clock = pygame.time.Clock()

font_size = int((screenParam[1] * 0.05))
fontc = pygame.font.Font(None, font_size)

running = True
pos = [0,0]

frameLimit = 60


RED = (255, 0, 0)
GRAY = (200, 200, 200)

#Power UI
slider_label_power = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((screenParam[0] * 0.05, screenParam[1] * 0.9625), (screenParam[0] * 0.05, screenParam[1] * 0.03)),
    text="Power",
    manager=ui_manager
)
sliderPower = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((screenParam[0] * 0.1, screenParam[1] * 0.9625), (screenParam[0] * 0.2, screenParam[1] * 0.03)),
    start_value=50,
    value_range=(0, 150),
    manager = ui_manager
)
slider_label_power_numerical = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((screenParam[0] * 0.3, screenParam[1] * 0.9625), (screenParam[0] * 0.05, screenParam[1] * 0.03)),
    text=str(sliderPower.get_current_value()),
    manager=ui_manager
)

#Angle UI
angle = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((screenParam[0] * 0.35, screenParam[1] * 0.9625), (screenParam[0] * 0.05, screenParam[1] * 0.03)),
    text="Angle",
    manager=ui_manager
)
sliderAngle = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((screenParam[0] * 0.4, screenParam[1] * 0.9625), (screenParam[0] * 0.2, screenParam[1] * 0.03)),
    start_value=50,
    value_range=(0, 180),
    manager = ui_manager
)
slider_label_angle_numerical = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((screenParam[0] * 0.6, screenParam[1] * 0.9625), (screenParam[0] * 0.05, screenParam[1] * 0.03)),
    text=str(sliderAngle.get_current_value()),
    manager=ui_manager
)

# Buttons
shootButton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((screenParam[0] * 0.85, screenParam[1] * 0.95), (screenParam[0] * 0.1, screenParam[1] * 0.05)),
    text="Shoot",
    manager=ui_manager
)

statButton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((screenParam[0] * 0.75, screenParam[1] * 0.95), (screenParam[0] * 0.1, screenParam[1] * 0.05)),
    text="Get Statistics",
    manager=ui_manager
)

#Setting up game level
levelGeometry = [(0,screenParam[1] * 0.8), (screenParam[0] * 0.3, screenParam[1] * 0.8),
                     (screenParam[0]* 0.5, screenParam[1] * 0.85), (screenParam[0]* 0.8, screenParam[1] * 0.75),
                     (screenParam[0], screenParam[1] * 0.75), (screenParam[0],screenParam[1] * 0.95),
                     (0,screenParam[1] * 0.95)]

tank0 = Tank.Tank(20,20,screenParam[0] * 0.1, screenParam[1] * 0.775, 0)
tank1 = Tank.Tank(20,20, screenParam[0] * 0.9, screenParam[1] * 0.725, 1)
tankList = [tank0, tank1]

cannonball = Cannonball.Cannonball(levelGeometry, 5, screenParam, tankList)

cannonball.SetPower(sliderPower.get_current_value())
cannonball.SetAngle(sliderAngle.get_current_value())

#Prepping dataAnalysis part
dataAnaliser = DataAnalysis.DataAnalysis(screenParam[0], screenParam[1])
dataAnaliser.dataget()


dataAnaliser.StartNewLevel()
#cannonball.quadratic_bezier([cannonball.start_x, cannonball.start_y], cannonball.GetPointInArc(10), cannonball.GetPointInArc(50))
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        ui_manager.process_events(event)
        if event.type == pygame.QUIT:
            dataAnaliser.EndLevel()
            dataAnaliser.EndGame()
            running = False
        
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == sliderPower:
                slider_label_power_numerical.set_text(str(sliderPower.get_current_value()))
                cannonball.SetPower(sliderPower.get_current_value())
            if event.ui_element == sliderAngle:
                slider_label_angle_numerical.set_text(str(sliderAngle.get_current_value()))
                cannonball.SetAngle(sliderAngle.get_current_value())

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == shootButton:
                if not cannonball.active:
                    dataAnaliser.AddShot()
                    cannonball.Shoot(float(sliderAngle.get_current_value()), float(sliderPower.get_current_value()))
            if event.ui_element == statButton:
                dataAnaliser.linreg()
                dataAnaliser.scatter()


    # Update the UI
    ui_manager.update(1/frameLimit)  # Delta time (e.g., 1/60 for 60 FPS)
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    pygame.draw.polygon(screen, (0,60,128), levelGeometry, 0)
    for tank in tankList:
        pygame.draw.rect(screen, (0,0,0), (tank.x, tank.y, tank.width,tank.height))
    
    if cannonball.GetActive():
        if cannonball.UpdatePointInArc(clock.get_time()):
            dataAnaliser.AddHit()
            dataAnaliser.EndLevel()
            dataAnaliser.StartNewLevel()
        pygame.draw.circle(screen, (128,75,0), cannonball.GetCurrentPosition(), cannonball.GetRadius())
    for looper in range(1,5):
        pygame.draw.circle(screen, (255,0,0), cannonball.GetPointInArc(looper * 500), cannonball.GetRadius() / 2)
    #Draw UI stuff
    points = [(0,screenParam[1] * 0.95), (screenParam[0], screenParam[1] * 0.95), (screenParam[0], screenParam[1]), (0,screenParam[1])]
    pygame.draw.polygon(screen, (0,0,0), points, 0)
    ui_manager.draw_ui(screen)
    counts = fontc.render("level: %d  shots: %d" % (dataAnaliser.currentLevels[len(dataAnaliser.currentLevels) - 1].levelId + 1, dataAnaliser.currentLevels[len(dataAnaliser.currentLevels) - 1].shots), True, (0, 0, 0))
    screen.blit(counts, (0, 0.0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(frameLimit)  # limits FPS to 60

pygame.quit()