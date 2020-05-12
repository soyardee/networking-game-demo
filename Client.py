import pygame

pygame.init()

window = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
run = True

def eventQueue(events):
    global run
    for event in events:
        if event.type == pygame.QUIT:
            run = False


while run:
    eventList = pygame.event.get()
    eventQueue(eventList)

    # run the game at 60 fps
    clock.tick(60)
    window.fill((0, 0, 0))

    pygame.display.update()

pygame.quit()

