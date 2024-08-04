import pygame
from pygame.locals import QUIT
from OpenGL.GL import (
    glClear,
    glMatrixMode,
    glLoadIdentity,
    glOrtho,
    GL_COLOR_BUFFER_BIT,
    GL_MODELVIEW,
    GL_PROJECTION,
)


class Visualisation:
    def __init__(self, environment):
        self.environment = environment
        pygame.init()
        display = (800, 800)
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, environment.size, 0, environment.size, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.environment.render()
        pygame.display.flip()
        # pygame.time.wait(10)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
