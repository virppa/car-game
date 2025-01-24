import os
import json
from colorama import Fore, Style
from car import Car, Part
from event import Event
from utils import clear_screen

# Ensure the save directory exists
SAVE_DIR = "saved_games"
os.makedirs(SAVE_DIR, exist_ok=True)

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

    def garage_menu(self):
        while True:
            clear_screen()
            print("=== Garage Menu ===")
            print("1. View Car Stats")
            print("2. Install Part")
            print("3. Uninstall Part")
            print("4. Return to Main Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_stats()
            elif choice == "2":
                self.install_part()
            elif choice == "3":
                self.uninstall_part()
            elif choice == "4":
                break
            else:
                print(Fore.RED + "Invalid choice. Try again." + Style.RESET_ALL)

    def uninstall_part(self):
        if not self.car.parts:
            print("No parts installed on the car to uninstall.")
            input("\nPress Enter to return to the garage...")
            return

        print("\n--- Installed Parts ---")
        for i, part in enumerate(self.car.parts):
            print(f"{i + 1}: {part.name} (Speed={part.speed}, Acceleration={part.acceleration}, Handling={part.handling}, Durability={part.durability}, Fuel Efficiency={part.fuel_efficiency})")

        try:
            choice = int(input("Enter the number of the part to uninstall: ")) - 1
            if 0 <= choice < len(self.car.parts):
                part = self.car.uninstall_part(choice)
                self.inventory.append(part)
                print(Fore.GREEN + f"Uninstalled {part.name}." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Invalid choice. Please select a valid part number." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number." + Style.RESET_ALL)
        input("\nPress Enter to return to the garage...")

    def main_menu(self):
        while not self.game_over:
            clear_screen()
            print("=== Strategic Car Game ===")
            print("1. Start Event")
            print("2. Garage")
            print("3. Save Game")
            print("4. Load Game")
            print("5. Exit Game")
            choice = input("Enter your choice: ")
            
            if choice == "1":
                self.play_turn()
                if not self.game_over:
                    self.install_part()
            elif choice == "2":
                self.garage_menu()
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
