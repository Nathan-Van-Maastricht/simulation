from OpenGL.GL import (
    glColor3f,
    glRectf,
)

import random


class Entity:
    def __init__(self, environment, x, y, name=None, colour=None):
        self.environment = environment
        self.x = x
        self.y = y
        if name is None:
            self.name = f"{type(self).__name__} {random.random()}"
        else:
            self.name = name
        self.colour = colour

    def render(self):
        if self.colour is not None:
            glColor3f(*self.colour)
            glRectf(self.x, self.y, self.x + 1, self.y + 1)

    def update(self):
        pass
