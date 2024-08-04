from OpenGL.GL import (
    glColor3f,
    glRectf,
)
import random


class BaseAgent:
    def __init__(
        self,
        environment,
        x,
        y,
        hunger_threshold=200,
        name=None,
        red=0.5,
        green=0.3,
        blue=0.1,
        pregnancy_duration=500,
        life_expectancy=2000,
    ):
        if name is None:
            self.name = f"{type(self).__name__} {random.random()}"
        else:
            self.name = name
        self.environment = environment
        self.x = x
        self.y = y
        self.directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]

        self.hunger_threshold = hunger_threshold * (1 + ((random.random() - 0.5) / 10))
        self.time_before_starve = self.hunger_threshold

        self.is_pregnant = False
        self.pregnancy_remaining = -1
        self.pregnancy_duration = pregnancy_duration * (
            1 + ((random.random() - 0.5) / 10)
        )

        self.life_expectancy = life_expectancy
        self.remaining_life = life_expectancy * (1 + ((random.random() - 0.5) / 10))

        self.red = red
        self.green = green
        self.blue = blue

    def update_starve(self):
        self.time_before_starve -= 1
        if self.time_before_starve <= 0:
            self.environment.agents.remove(self)
            print(f"{self.name} has starved at iteration {self.environment.iteration}")
            del self
            return True

    def update_pregnancy(self):
        self.pregnancy_remaining -= 1

        if self.pregnancy_remaining <= 0:
            self.is_pregnant = False
            self.pregnancy_remaining = -1

            child_x = self.x + (-(1 ** random.randint(0, 1))) * random.randint(1, 2)
            child_y = self.y + (-(1 ** random.randint(0, 1))) * random.randint(1, 2)

            child = type(self)(
                self.environment,
                child_x,
                child_y,
                red=max(0, min(self.red + (random.random() - 0.5) / 10, 1)),
                green=max(0, min(self.green + (random.random() - 0.5) / 10, 1)),
                blue=max(0, min(self.blue + (random.random() - 0.5) / 10, 1)),
            )

            self.environment.add_agent(child)

            print(f"{self.name} has given birth to {child.name}!")

    def update_life(self):
        self.remaining_life -= 1
        if self.remaining_life <= 0:
            self.environment.agents.remove(self)
            print(
                f"{self.name} has died of old age at iteration {self.environment.iteration}"
            )
            del self
            return True

    def update(self):
        if self.update_starve():
            return

        if self.is_pregnant:
            self.update_pregnancy()

        self.update_life()
        self.move()

    def move(self):
        dx, dy = random.choice(self.directions)

        self.x = (self.x + dx) % self.environment.size
        self.y = (self.y + dy) % self.environment.size

    def fall_pregnant(self):
        self.pregnancy_remaining = self.pregnancy_duration
        self.is_pregnant = True

    def render(self):
        glColor3f(self.red, self.green, self.blue)
        glRectf(self.x, self.y, self.x + 1, self.y + 1)
