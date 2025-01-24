import random

class Car:
    def __init__(self):
        self.speed = 50
        self.acceleration = 50
        self.handling = 50
        self.durability = 100
        self.fuel_efficiency = 50
        self.parts = []

    def install_part(self, part):
        self.parts.append(part)
        self.speed += part.speed
        self.acceleration += part.acceleration
        self.handling += part.handling
        self.durability += part.durability
        self.fuel_efficiency += part.fuel_efficiency

    def take_damage(self, damage):
        self.durability -= damage

    def is_destroyed(self):
        return self.durability <= 0

class Part:
    def __init__(self, name, speed=0, acceleration=0, handling=0, durability=0, fuel_efficiency=0):
        self.name = name
        self.speed = speed
        self.acceleration = acceleration
        self.handling = handling
        self.durability = durability
        self.fuel_efficiency = fuel_efficiency

class Event:
    def __init__(self, name, difficulty, reward):
        self.name = name
        self.difficulty = difficulty
        self.reward = reward

    def compete(self, car):
        print(f"Event: {self.name}")
        print(f"Difficulty: {self.difficulty}")
        
        # Calculate success chance
        success_chance = (car.speed + car.handling + car.acceleration) / (self.difficulty * 100)
        success_roll = random.random()

        if success_roll < success_chance:
            print("You succeeded in the event!")
            return True
        else:
            damage = random.randint(10, 30)
            print(f"You failed the event and took {damage} damage.")
            car.take_damage(damage)
            return False

class Game:
    def __init__(self):
        self.car = Car()
        self.inventory = []
        self.events = [
            Event("Drag Race", difficulty=2, reward=Part("Turbocharger", speed=20, acceleration=10)),
            Event("Off-Road Rally", difficulty=3, reward=Part("All-Terrain Tires", handling=15, durability=10)),
            Event("Endurance Race", difficulty=4, reward=Part("Fuel Saver", fuel_efficiency=20))
        ]
        self.game_over = False

    def play_turn(self):
        print("\n--- New Turn ---")
        print(f"Car Stats: Speed={self.car.speed}, Acceleration={self.car.acceleration}, Handling={self.car.handling}, Durability={self.car.durability}, Fuel Efficiency={self.car.fuel_efficiency}")
        
        # Choose an event
        print("Choose an event:")
        for i, event in enumerate(self.events):
            print(f"{i + 1}: {event.name} (Difficulty: {event.difficulty})")
        choice = int(input("Enter the number of the event: ")) - 1

        if 0 <= choice < len(self.events):
            event = self.events[choice]
            success = event.compete(self.car)

            if success:
                print(f"You earned the reward: {event.reward.name}")
                self.inventory.append(event.reward)

        if self.car.is_destroyed():
            self.game_over = True
            print("Your car is destroyed. Game over!")

    def install_part(self):
        print("\n--- Inventory ---")
        for i, part in enumerate(self.inventory):
            print(f"{i + 1}: {part.name} (Speed={part.speed}, Acceleration={part.acceleration}, Handling={part.handling}, Durability={part.durability}, Fuel Efficiency={part.fuel_efficiency})")
        choice = int(input("Enter the number of the part to install: ")) - 1

        if 0 <= choice < len(self.inventory):
            part = self.inventory.pop(choice)
            self.car.install_part(part)
            print(f"Installed {part.name}.")

    def run(self):
        print("Welcome to the Strategic Car Game!")
        while not self.game_over:
            self.play_turn()
            if not self.game_over:
                self.install_part()
        print("Thanks for playing!")

# Start the game
game = Game()
game.run()
