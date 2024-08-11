from agents.baseagent import BaseAgent

import random


class Human(BaseAgent):
    def __init__(
        self,
        environment,
        x,
        y,
        name=None,
        colour=(0, 0, 0.9),
        hunger_threshold=200,
        pregnancy_duration=200,
        life_expectancy=1500,
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
            self.environment.stats.humans_starved += 1
            return True

    def update_pregnancy(self):
        super().update_pregnancy()
        if not self.is_pregnant:
            self.environment.stats.human_births += 1

    def update(self):
        super().update()

    def move(self):
        if self.time_before_starve < 50:
            nearest_food = self.environment.get_nearest_food(self.x, self.y)
            if nearest_food:
                dx = nearest_food.x - self.x
                dy = nearest_food.y - self.y
                if dx != 0:
                    self.x += dx // abs(dx)
                if dy != 0:
                    self.y += dy // abs(dy)

                self.x = min(self.environment.size, max(0, self.x))
                self.y = min(self.environment.size, max(0, self.y))

                return
        elif (
            not self.is_pregnant
            and self.remaining_life < 2 * self.life_expectancy / 3
            and self.remaining_life > self.life_expectancy / 3
        ):
            nearest_human = self.environment.find_nearest_human(self)
            if nearest_human is not None:
                dx = nearest_human.x - self.x
                dy = nearest_human.y - self.y
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

    def fall_pregnant(self):
        super().fall_pregnant()
        self.environment.stats.human_pregnancies += 1

    def update_life(self):
        if super().update_life():
            self.environment.stats.humans_old_age += 1
            return True
