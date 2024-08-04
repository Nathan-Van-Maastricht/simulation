from environment.environment import Environment
from environment.visualisation import Visualisation
from agents.human import Human
from agents.bear import Bear

import random


def main():
    size = 150
    environment = Environment(size)
    visualization = Visualisation(environment)

    for i in range(size):
        for j in range(size):
            random_number = random.random()
            match random_number:
                case x if x < 0.098:
                    environment.add_food(i, j)
                case x if x < 0.1125:
                    environment.add_agent(
                        Human(
                            environment,
                            random.randint(0, size),
                            random.randint(0, size),
                        )
                    )
                case x if x < 0.12:
                    environment.add_agent(
                        Bear(
                            environment,
                            random.randint(0, size),
                            random.randint(0, size),
                        )
                    )

    while True:
        visualization.handle_events()
        environment.update()
        visualization.render()
        if len(environment.agents) == 0:
            print(environment.stats)
            break


if __name__ == "__main__":
    main()
