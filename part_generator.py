import random
from part import Part

RARITY_LEVELS = {
    "Common": {"min_stat": 1, "max_stat": 5, "trait_chance": 0.1},
    "Rare": {"min_stat": 5, "max_stat": 10, "trait_chance": 0.3},
    "Epic": {"min_stat": 10, "max_stat": 15, "trait_chance": 0.5},
    "Legendary": {"min_stat": 15, "max_stat": 20, "trait_chance": 0.8}
}

TRAITS = [
    "Fuel Saver", "Drift King", "Turbo Boost", "Off-Road Expert", "Lightweight Design"
]

PART_TYPES = ["Engine", "Tires", "Brakes", "Suspension", "Exhaust"]

def generate_part():
    part_type = random.choice(PART_TYPES)
    rarity = random.choice(list(RARITY_LEVELS.keys()))
    rarity_data = RARITY_LEVELS[rarity]
    
    stats = {
        "speed": random.randint(rarity_data["min_stat"], rarity_data["max_stat"]),
        "acceleration": random.randint(rarity_data["min_stat"], rarity_data["max_stat"]),
        "handling": random.randint(rarity_data["min_stat"], rarity_data["max_stat"]),
        "durability": random.randint(rarity_data["min_stat"], rarity_data["max_stat"]),
        "fuel_efficiency": random.randint(rarity_data["min_stat"], rarity_data["max_stat"])
    }
    
    # Assign the trait
    trait = random.choice(TRAITS) if random.random() < rarity_data["trait_chance"] else None
    
    return Part(
        name=f"{rarity} {part_type}",
        speed=stats["speed"],
        acceleration=stats["acceleration"],
        handling=stats["handling"],
        durability=stats["durability"],
        fuel_efficiency=stats["fuel_efficiency"],
        trait=trait
    )


def generate_parts(num_parts=10):
    return [generate_part() for _ in range(num_parts)]
