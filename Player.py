import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.boundsX = pygame.display.get_surface().get_width()
        self.boundsY = pygame.display.get_surface().get_height()

        # how far each player moves each frame
        # use this in the server to "guess" where a person is going given connection drops
        self.x_vel = 1
        self.y_vel = 1

    def get_rectangle(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self, window):
        pygame.draw.rect(window, self.color, self.get_rectangle())

    # data received from the server to move
    def move(self, keys):
        # python does not support switch case
        # TODO process this outside of the player class, as we need to send this info to the server.
        if keys[pygame.K_A] and self.x > 0:
            self.x -= self.x_vel
        if keys[pygame.K_D] and self.x + self.width < self.boundsX:
            self.x += self.x_vel
        if keys[pygame.K_W] and self.y > 0:
            self.y -= self.y_vel
        if keys[pygame.K_S] and self.y + self.height < self.boundsY:
            self.y += self.y_vel


