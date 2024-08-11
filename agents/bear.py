from agents.baseagent import BaseAgent

import random


class Bear(BaseAgent):
    def __init__(
        self,
        environment,
        x,
        y,
        hunger_threshold=300,
        name=None,
        colour=(0.0, 0.0, 0.0),
        pregnancy_duration=500,
        life_expectancy=2000,
    ):
        super().__init__(
            environment,
            x,
            y,
            name,
            colour,
            hunger_threshold,
            pregnancy_duration,
            life_expectancy,
        )

    def update_starve(self):
        if super().update_starve():
            self.environment.stats.bears_starved += 1
            return True

    def update_pregnancy(self):
        super().update_pregnancy()
        if not self.is_pregnant:
            self.environment.stats.bear_births += 1

    def update_life(self):
        if super().update_life():
            self.environment.stats.bears_old_age += 1
            return True

    def move(self):
        if self.time_before_starve < 100:
            nearest_human = self.environment.find_nearest_human(self)
            if not self.is_pregnant and nearest_human is not None:
                dx = nearest_human.x - self.x
                dy = nearest_human.y - self.y
                if random.random() < 0.5:
                    if dx != 0:
                        self.x += dx // abs(dx)
                    elif dy != 0:
                        self.y += dy // abs(dy)
                else:
                    if dy != 0:
                        self.y += dy // abs(dy)
                    elif dx != 0:
                        self.x += dx // abs(dx)

                self.x = min(self.environment.size, max(0, self.x))
                self.y = min(self.environment.size, max(0, self.y))

                return
        elif (
            not self.is_pregnant
            and self.remaining_life < 2 * self.life_expectancy / 3
            and self.remaining_life > self.life_expectancy / 3
        ):
            nearest_bear = self.environment.find_nearest_bear(self)
            if nearest_bear is not None:
                dx = nearest_bear.x - self.x
                dy = nearest_bear.y - self.y
                if dx != 0:
                    dx //= abs(dx)
                if dy != 0:
                    dy //= abs(dy)

                rotation = random.choice([-1, 0, 1])
                if rotation == -1:  # Rotate by -45 degrees
                    dx, dy = -dy, dx
                elif rotation == 1:  # Rotate by 45 degrees
                    dx, dy = dy, -dx

                self.x += dx
                self.y += dy

                self.x = min(self.environment.size, max(0, self.x))
                self.y = min(self.environment.size, max(0, self.y))
                return

        super().move()

    def update(self):
        super().update()

    def fall_pregnant(self):
        super().fall_pregnant()
        self.environment.stats.bear_pregnancies += 1
