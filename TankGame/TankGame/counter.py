import pygame as py

# Initialize Pygame
py.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Data Analysis")


level = 1
shots = 1
screen.fill((255, 255, 255))



def counter(): #need to find a way where the screen doesn't update over the projectile.
#maybe a new variable called finished shots which updates when it impacts or goes off screen
#we can set it to 0 after every level too
    screen.fill((255, 255, 255))

    #draw static image code here

    WIDTH_N = WIDTH - (1/4 * WIDTH)
    HEIGHT_N = HEIGHT - (15/16 * HEIGHT)
    font_size = int((HEIGHT * 0.05))
    fontc = py.font.Font(None, font_size)
    counts = fontc.render("level: %d  shots: %d" % (level, shots), True, (0, 0, 0))
    screen.blit(counts, (WIDTH_N, HEIGHT_N))
    py.display.flip()


#--do not import this. this is for testing--
def on_key_c(event):
    global level, shots
    if event.key == py.K_l:  
        level += 1
        counter()
    if event.key == py.K_s:
        shots += 1
        counter()

counter()
running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.KEYDOWN:
            on_key_c(event)
py.quit()