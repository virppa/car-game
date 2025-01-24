from part import Part

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

    def uninstall_part(self, part_index):
        if 0 <= part_index < len(self.parts):
            part = self.parts.pop(part_index)
            self.speed -= part.speed
            self.acceleration -= part.acceleration
            self.handling -= part.handling
            self.durability -= part.durability
            self.fuel_efficiency -= part.fuel_efficiency
            return part
        else:
            raise IndexError("Invalid part index.")

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
