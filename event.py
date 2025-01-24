import random
from colorama import Fore, Style

class Event:
    def __init__(self, name, difficulty, reward):
        self.name = name
        self.difficulty = difficulty
        self.reward = reward
        self.modifier = self.generate_modifier()

    def generate_modifier(self):
        modifiers = [
            {"name": "Rainy Weather", "handling_penalty": 10},
            {"name": "Icy Roads", "handling_penalty": 20},
            {"name": "Hot Weather", "durability_penalty": 15},
            {"name": "High Winds", "speed_penalty": 10},
            {"name": "Clear Skies", "boost": 10},
        ]
        return random.choice(modifiers)

    def apply_modifier(self, car):
        if "handling_penalty" in self.modifier:
            car.handling -= self.modifier["handling_penalty"]
        if "durability_penalty" in self.modifier:
            car.durability -= self.modifier["durability_penalty"]
        if "speed_penalty" in self.modifier:
            car.speed -= self.modifier["speed_penalty"]
        if "boost" in self.modifier:
            car.speed += self.modifier["boost"]

    def compete(self, car):
        print(f"Event: {self.name}")
        print(f"Difficulty: {self.difficulty}")
        print(f"Modifier: {self.modifier['name']}")

        self.apply_modifier(car)
        
        # Calculate success chance
        success_chance = max(0.1, min((car.speed + car.handling + car.acceleration) / (self.difficulty * 100), 1))
        success_roll = random.random()

        if success_roll < success_chance:
            print(Fore.GREEN + "You succeeded in the event!" + Style.RESET_ALL)
            return True
        else:
            damage = random.randint(10 * self.difficulty, 30 * self.difficulty)
            print(Fore.RED + f"You failed the event and took {damage} damage." + Style.RESET_ALL)
            car.take_damage(damage)
            return False