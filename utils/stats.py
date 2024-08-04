class Stats:
    def __init__(self):
        self.human_pregnancies = 0
        self.bear_pregnancies = 0

        self.human_births = 0
        self.bear_births = 0

        self.food_consumed = 0
        self.bear_attacks = 0

        self.humans_starved = 0
        self.bears_starved = 0

        self.humans_old_age = 0
        self.bears_old_age = 0

    def __str__(self):
        return f"Human Pregnancies: {self.human_pregnancies}\nBear Pregnancies: {self.bear_pregnancies}\nHuman Births: {self.human_births}\nBear Births: {self.bear_births}\nFood Consumed: {self.food_consumed}\nBear Attacks: {self.bear_attacks}\nHumans Starved: {self.humans_starved}\nBears Starved: {self.bears_starved}\nHumans died of old age: {self.humans_old_age}\nBears died of old age: {self.bears_old_age}"
