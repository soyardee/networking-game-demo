import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        # how far each player moves each frame
        # use this in the server to "guess" where a person is going given connection drops
        self.x_vel = 1
        self.y_vel = 1

    def get_rectangle(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self, window):
        pygame.draw.rect(window, self.color, self.get_rectangle())

    # data received from the server to move
    def move(self, direction, bounds):
        # python does not support switch case
        if "W" in direction and self.x > 0:
            self.x -= self.x_vel
        if "E" in direction and self.x + self.width < bounds[0]:
            self.x += self.x_vel
        if "N" in direction and self.y > 0:
            self.y -= self.y_vel
        if "S" in direction and self.y + self.height < bounds[1]:
            self.y += self.y_vel


