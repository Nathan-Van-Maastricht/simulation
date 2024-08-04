from environment.environment import Environment
from environment.visualisation import Visualisation
from utils.config import load_config


def main():
    config = load_config("config.json")
    environment = Environment(config)
    visualization = Visualisation(environment)

    while True:
        visualization.handle_events()
        environment.update()
        visualization.render()
        if len(environment.agents) == 0:
            print(environment.stats)
            break


if __name__ == "__main__":
    main()
