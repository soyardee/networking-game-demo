import pygame
from NetworkAdapter import Network
from Player import Player

pygame.init()
n = Network("73.37.174.96", 9652)

font = pygame.font.SysFont('Courier New', 40)
window = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
run = False


def eventQueue(events):
    global run
    for event in events:
        if event.type == pygame.QUIT:
            run = False

def draw_loading_screen():
    window.fill((255, 255, 255))
    surface = font.render("Connecting", False, (255,0,0))
    window.blit(surface, (0, 0))
    pygame.display.update()

def draw_screen(player_data):
    window.fill((255, 255, 255))

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


def init_connection():
    global run
    draw_loading_screen()
    while not n.ready:
        n.connect()
    run = True


def main():
    init_connection()
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

main()

