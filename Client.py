import pygame
from NetworkAdapter import Network
from Player import Player

pygame.init()
n = Network("127.0.0.1", 1234)


window = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
run = True


def eventQueue(events):
    global run
    for event in events:
        if event.type == pygame.QUIT:
            run = False


def draw_screen(player_data):
    window.fill((0, 0, 0))

    for p in player_data:
        p.render(window)

    pygame.display.update()

def movement(keys):
    command = ""
    if keys[pygame.K_UP]:
        command += 'N'
    if keys[pygame.K_RIGHT]:
        command += 'E'
    if keys[pygame.K_DOWN]:
        command += 'S'
    if keys[pygame.K_LEFT]:
        command += 'W'

    n.move(command)

while not n.ready:
    n.connect()

while run:
    # run the game at 60 fps
    clock.tick(60)

    players = n.get_players()
    eventList = pygame.event.get()
    keys = pygame.key.get_pressed()
    movement(keys)


    eventQueue(eventList)
    draw_screen(players)


n.disconnect()
pygame.quit()

