class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        """Add an item to the inventory."""
        self.items.append(item)

    def remove_item(self, index):
        """Remove and return an item from the inventory."""
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        raise IndexError("Invalid inventory index.")

    def is_empty(self):
        """Check if the inventory is empty."""
        return len(self.items) == 0

    def __str__(self):
        """Generate a string representation of the inventory."""
        inventory_str = "\n--- Inventory ---\n"
        for i, item in enumerate(self.items):
            inventory_str += f"{i + 1}: {item.name} (Speed={item.speed}, Acceleration={item.acceleration}, Handling={item.handling}, Durability={item.durability}, Fuel Efficiency={item.fuel_efficiency})\n"
        return inventory_str.strip()
