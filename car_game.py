import random
import os
import json
from colorama import Fore, Style

# Utility function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Ensure the save directory exists
SAVE_DIR = "saved_games"
os.makedirs(SAVE_DIR, exist_ok=True)

class Car:
    def __init__(self):
        self.speed = 50
        self.acceleration = 50
        self.handling = 50
        self.durability = 100
        self.fuel_efficiency = 50
        self.parts = []

    def install_part(self, part):
        if not isinstance(part, Part):
            raise ValueError("Invalid part. Expected an instance of Part.")
        self.parts.append(part)
        self.speed += part.speed
        self.acceleration += part.acceleration
        self.handling += part.handling
        self.durability += part.durability
        self.fuel_efficiency += part.fuel_efficiency

    def to_dict(self):
        return {
            "speed": self.speed,
            "acceleration": self.acceleration,
            "handling": self.handling,
            "durability": self.durability,
            "fuel_efficiency": self.fuel_efficiency,
            "parts": [part.name for part in self.parts]
        }

    def from_dict(self, data):
        self.speed = data["speed"]
        self.acceleration = data["acceleration"]
        self.handling = data["handling"]
        self.durability = data["durability"]
        self.fuel_efficiency = data["fuel_efficiency"]
        self.parts = [Part(name) for name in data["parts"]]
   
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

    def save_game(self, slot_number):
        data = {
            "car": self.car.to_dict(),
            "inventory": [part.name for part in self.inventory]
        }
        filename = os.path.join(SAVE_DIR, f"save_slot_{slot_number}.json")
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print(Fore.GREEN + f"Game saved to slot {slot_number}." + Style.RESET_ALL)

    def load_game(self, slot_number):
        filename = os.path.join(SAVE_DIR, f"save_slot_{slot_number}.json")
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self.car.from_dict(data["car"])
                self.inventory = [Part(name) for name in data["inventory"]]
            print(Fore.GREEN + f"Game loaded from slot {slot_number}." + Style.RESET_ALL)
        except FileNotFoundError:
            print(Fore.RED + f"No save file found in slot {slot_number}." + Style.RESET_ALL)

    def view_stats(self):
        clear_screen()
        print("=== Car Stats ===")
        print(f"Speed: {self.car.speed}")
        print(f"Acceleration: {self.car.acceleration}")
        print(f"Handling: {self.car.handling}")
        print(f"Durability: {self.car.durability}")
        print(f"Fuel Efficiency: {self.car.fuel_efficiency}")
        print(f"Parts Installed: {[part.name for part in self.car.parts]}")
        input("\nPress Enter to return to the main menu...")

    def main_menu(self):
        while not self.game_over:
            clear_screen()
            print("=== Strategic Car Game ===")
            print("1. Start Event")
            print("2. View Car Stats")
            print("3. Save Game")
            print("4. Load Game")
            print("5. Exit Game")
            choice = input("Enter your choice: ")
            
            if choice == "1":
                self.play_turn()
                if not self.game_over:
                    self.install_part()
            elif choice == "2":
                self.view_stats()
            elif choice == "3":
                slot = int(input("Enter save slot (1-3): "))
                if 1 <= slot <= 3:
                    self.save_game(slot)
                else:
                    print(Fore.RED + "Invalid slot number. Please choose between 1 and 3." + Style.RESET_ALL)
            elif choice == "4":
                slot = int(input("Enter save slot to load (1-3): "))
                if 1 <= slot <= 3:
                    self.load_game(slot)
                else:
                    print(Fore.RED + "Invalid slot number. Please choose between 1 and 3." + Style.RESET_ALL)
            elif choice == "5":
                print("Thanks for playing!")
                break
            else:
                print(Fore.RED + "Invalid choice. Try again." + Style.RESET_ALL)

    def play_turn(self):
        clear_screen()
        print("\n--- New Turn ---")
        print(f"Car Stats: Speed={self.car.speed}, Acceleration={self.car.acceleration}, Handling={self.car.handling}, Durability={self.car.durability}, Fuel Efficiency={self.car.fuel_efficiency}")
        
        # Choose an event
        print("Choose an event:")
        for i, event in enumerate(self.events):
            print(f"{i + 1}: {event.name} (Difficulty: {event.difficulty}, Modifier: {event.modifier['name']}) - Reward: {event.reward.name}")
        try:
            choice = int(input("Enter the number of the event: ")) - 1
            if 0 <= choice < len(self.events):
                event = self.events[choice]
                success = event.compete(self.car)

                if success:
                    print(Fore.GREEN + f"You earned the reward: {event.reward.name}" + Style.RESET_ALL)
                    self.inventory.append(event.reward)
            else:
                print(Fore.RED + "Invalid choice. Please select a valid event number." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number." + Style.RESET_ALL)

        if self.car.is_destroyed():
            self.game_over = True
            print(Fore.RED + "Your car is destroyed. Game over!" + Style.RESET_ALL)
            print("Final Performance Summary:")
            print(f"Speed: {self.car.speed}, Acceleration: {self.car.acceleration}, Handling: {self.car.handling}, Durability: {self.car.durability}, Fuel Efficiency: {self.car.fuel_efficiency}")
            print(f"Parts installed: {[part.name for part in self.car.parts]}")

    def install_part(self):
        if not self.inventory:
            print("Your inventory is empty. No parts available to install.")
            input("\nPress Enter to return to the main menu...")
            return

        print("\n--- Inventory ---")
        print(f"{'Index':<5}{'Part Name':<20}{'Stats':<30}")
        for i, part in enumerate(self.inventory):
            stats = f"Speed={part.speed}, Acc={part.acceleration}, Handling={part.handling}"
            print(f"{i + 1:<5}{part.name:<20}{stats:<30}")
        try:
            choice = int(input("Enter the number of the part to install: ")) - 1
            if 0 <= choice < len(self.inventory):
                part = self.inventory.pop(choice)
                self.car.install_part(part)
                print(Fore.GREEN + f"Installed {part.name}." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Invalid choice. Please select a valid part number." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number." + Style.RESET_ALL)

    def run(self):
        print("Welcome to the Strategic Car Game!")
        self.main_menu()

# Start the game
game = Game()
game.run()
