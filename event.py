import random
from colorama import Fore, Style
from part_generator import generate_part_with_rarity
from constants import EVENT_MODIFIERS

class Event:
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty
        self.modifier = self.generate_modifier()
        self.reward = self.generate_reward()

    def generate_modifier(self):
        modifiers = EVENT_MODIFIERS
        return random.choice(modifiers)

    def generate_reward(self):
        # Define weight multipliers for rarities based on event difficulty
        rarity_weights = {
            "Common": max(10 - self.difficulty * 2, 1),  # Higher difficulty decreases Common likelihood
            "Rare": max(self.difficulty * 2, 1),
            "Epic": max(self.difficulty - 2, 1) if self.difficulty > 2 else 0,
            "Legendary": max(self.difficulty - 4, 1) if self.difficulty > 4 else 0,
        }

        # Filter rarities with zero weight
        rarities = [rarity for rarity, weight in rarity_weights.items() if weight > 0]
        weights = [rarity_weights[rarity] for rarity in rarities]

        # Select a weighted random rarity
        selected_rarity = random.choices(rarities, weights=weights, k=1)[0]

        # Generate a part with the selected rarity
        part = generate_part_with_rarity(selected_rarity)
        print(f"Generated reward for {self.name}: {part}")  # Debug line
        return part

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
        print(f"Reward: {self.reward}")

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
