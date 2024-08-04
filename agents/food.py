from agents.entity import Entity

import random


class Food(Entity):
    def __init__(self, environment, x, y, name=None, colour=(1, 0, 0)):
        super().__init__(environment, x, y, name, colour)

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y

    def __hash__(self):
        return (self.x, self.y).__hash__()

    def __str__(self):
        return f"{self.name}, ({self.x}, {self.y})"

    def update(self):
        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (-1, -1),
            (1, -1),
            (-1, 1),
        ]
        if random.random() < self.environment.config["food_spawn_rate"]:
            random.shuffle(directions)
            for dx, dy in directions:
                new_x, new_y = (
                    (self.x + dx) % self.environment.size,
                    (self.y + dy) % self.environment.size,
                )
                if (new_x, new_y) not in self.environment.food_index2id and (
                    new_x,
                    new_y,
                ) not in [(agent.x, agent.y) for agent in self.environment.agents]:
                    self.environment.add_food(new_x, new_y)
                    break
