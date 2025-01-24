class Part:
    def __init__(self, name, speed=0, acceleration=0, handling=0, durability=0, fuel_efficiency=0, trait=None):
        self.name = name
        self.speed = speed
        self.acceleration = acceleration
        self.handling = handling
        self.durability = durability
        self.fuel_efficiency = fuel_efficiency
        self.trait = trait

    def __repr__(self):
        return (f"Part({self.name}, Speed={self.speed}, Accel={self.acceleration}, "
                f"Handling={self.handling}, Durability={self.durability}, "
                f"Fuel={self.fuel_efficiency}, Trait={self.trait})")
