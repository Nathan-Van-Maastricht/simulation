import pygame
from pygame.locals import QUIT, MOUSEWHEEL, MOUSEMOTION
from OpenGL.GL import (
    glClear,
    glMatrixMode,
    glLoadIdentity,
    glScalef,
    glTranslatef,
    GL_COLOR_BUFFER_BIT,
    GL_MODELVIEW,
)
from OpenGL.GLU import gluPerspective


class Visualisation:
    def __init__(self, environment):
        self.environment = environment
        pygame.init()
        display = (800, 800)
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        self.zoom = 1
        self.offset = [0, 0]

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glScalef(self.zoom, self.zoom, 1)
        glTranslatef(self.offset[0], self.offset[1], 0)
        self.environment.render()
        pygame.display.flip()
        # pygame.time.wait(10)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == MOUSEWHEEL:
                self.zoom += event.y * 0.1
                if self.zoom < 0.1:
                    self.zoom = 0.1
            elif event.type == MOUSEMOTION and event.buttons[0]:
                self.offset[0] += event.rel[0] / self.zoom
                self.offset[1] += event.rel[1] / self.zoom
