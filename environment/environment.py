from OpenGL.GL import (
    glClear,
    glMatrixMode,
    glLoadIdentity,
    glOrtho,
    glColor3f,
    glRectf,
    GL_COLOR_BUFFER_BIT,
    GL_PROJECTION,
    GL_MODELVIEW,
)
import random
import bisect

from agents.human import Human
from agents.bear import Bear
from utils.stats import Stats

from rtree import index


class Environment:
    def __init__(self, config):
        self.size = config["size"]
        self.agents = []

        self.food_index = index.Index()
        self.food_index2id = {}
        self.food_id2index = {}
        self.total_foods = 0

        self.iteration = 0

        self.stats = Stats()
        self.config = config

        self.spawn_initial_agents()

    def spawn_initial_agents(self):
        cumulative_percentages = [0]
        functions = {
            "food": lambda *args: self.add_food(args[0], args[1]),
            "humans": lambda *args: self.add_agent(
                Human(
                    self,
                    random.randint(0, self.size),
                    random.randint(0, self.size),
                )
            ),
            "bears": lambda *args: self.add_agent(
                Bear(
                    self,
                    random.randint(0, self.size),
                    random.randint(0, self.size),
                )
            ),
        }
        percentages = {
            "food": self.config["percent_food"],
            "humans": self.config["percent_human"],
            "bears": self.config["percent_bear"],
        }
        for percentage in percentages.values():
            cumulative_percentages.append(cumulative_percentages[-1] + percentage)

        keys = list(percentages.keys())

        for i in range(self.size):
            for j in range(self.size):
                random_number = random.random()
                if random_number <= cumulative_percentages[-1]:
                    index = bisect.bisect_left(cumulative_percentages, random_number)
                    matched_key = keys[index - 1]
                    functions[matched_key](i, j)

    def add_agent(self, agent):
        self.agents.append(agent)

    def find_nearest_human(self, agent_start):
        nearest_agent = None
        min_distance = float("inf")
        for agent in self.agents:
            if agent == agent_start:
                continue
            if isinstance(agent, Human):
                dx = abs(agent.x - agent.x)
                dy = abs(agent.y - agent.y)
                # Consider wrap-around
                dx = min(dx, self.size - dx)
                dy = min(dy, self.size - dy)
                distance = dx**2 + dy**2
                if distance < min_distance:
                    min_distance = distance
                    nearest_agent = agent
        return nearest_agent

    def find_nearest_bear(self, agent_start):
        nearest_agent = None
        min_distance = float("inf")
        for agent in self.agents:
            if agent == agent_start:
                continue
            if isinstance(agent, Bear):
                dx = abs(agent.x - agent.x)
                dy = abs(agent.y - agent.y)
                # Consider wrap-around
                dx = min(dx, self.size - dx)
                dy = min(dy, self.size - dy)
                distance = dx**2 + dy**2
                if distance < min_distance:
                    min_distance = distance
                    nearest_agent = agent
        return nearest_agent

    def add_food(self, food_x, food_y):
        self.food_index2id[(food_x, food_y)] = self.total_foods
        self.food_id2index[self.total_foods] = (food_x, food_y)
        self.food_index.insert(self.total_foods, (food_x, food_y, food_x, food_y))

        self.total_foods += 1

    def remove_food(self, coordinates):
        food_id = self.food_index2id.pop(coordinates, None)
        self.food_id2index.pop(food_id)
        if food_id is not None:
            self.food_index.delete(food_id, (*coordinates, *coordinates))

    def get_nearest_food(self, x, y):
        nearest_foods = list(self.food_index.nearest((x, y, x, y), 1))
        if len(nearest_foods):
            return self.food_id2index[nearest_foods[0]]
        return None

    def update(self):
        for agent in self.agents:
            agent.update()

        for agent in self.agents:
            for other_agent in self.agents:
                if agent == other_agent:
                    continue

                if type(agent) is type(other_agent):
                    if agent.is_pregnant or other_agent.is_pregnant:
                        continue

                    if agent.x == other_agent.x and agent.y == other_agent.y:
                        mother = random.choice([agent, other_agent])
                        mother.fall_pregnant()
                        print(
                            f"{mother.name} is pregnant on iteration {self.iteration}"
                        )
                elif (
                    isinstance(agent, Bear)
                    and isinstance(other_agent, Human)
                    and agent.x == other_agent.x
                    and agent.y == other_agent.y
                ):
                    self.stats.bear_attacks += 1
                    print(
                        f"{agent.name} has eaten {other_agent.name} at iteration {self.iteration}"
                    )
                    self.agents.remove(other_agent)
                    del other_agent
                    agent.time_before_starve = agent.hunger_threshold

            if isinstance(agent, Human):
                nearest_food = self.get_nearest_food(agent.x, agent.y)
                if nearest_food is not None:
                    if agent.x == nearest_food[0] and agent.y == nearest_food[1]:
                        self.stats.food_consumed += 1
                        agent.time_before_starve = agent.hunger_threshold
                        self.remove_food(nearest_food)

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
        for food_x, food_y in list(self.food_index2id.keys()):
            if random.random() < self.config["food_spawn_rate"]:
                random.shuffle(directions)
                for dx, dy in directions:
                    new_x, new_y = (food_x + dx) % self.size, (food_y + dy) % self.size
                    if (new_x, new_y) not in self.food_index2id and (
                        new_x,
                        new_y,
                    ) not in [(agent.x, agent.y) for agent in self.agents]:
                        self.add_food(new_x, new_y)
                        break

        self.iteration += 1

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.size, 0, self.size, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Render environment
        glColor3f(0.196, 0.588, 0.278)  # Green
        glRectf(0, 0, self.size, self.size)

        # render food
        glColor3f(1, 0, 0)
        for x, y in self.food_id2index.values():
            glRectf(x, y, x + 1, y + 1)

        for agent in self.agents:
            agent.render()
