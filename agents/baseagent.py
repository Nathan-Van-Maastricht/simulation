import random

from agents.entity import Entity


class BaseAgent(Entity):
    def __init__(
        self,
        environment,
        x,
        y,
        name=None,
        colour=None,
        hunger_threshold=200,
        pregnancy_duration=500,
        life_expectancy=2000,
    ):
        super().__init__(environment, x, y, name, colour)

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
                colour=(
                    max(0, min(self.red + (random.random() - 0.5) / 10, 1)),
                    max(0, min(self.green + (random.random() - 0.5) / 10, 1)),
                    max(0, min(self.blue + (random.random() - 0.5) / 10, 1)),
                ),
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
