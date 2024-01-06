class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            print(f'Added {item.item_id} to inventory')
            return True
        else:
            return False  # Inventory is full

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f'Removed {item.name} from inventory')
            return True
        else:
            return False  # Item not found in inventory

    def get_items(self):
        return self.items
    
    def get_capacity(self):
        return self.capacity

    def is_full(self):
        return len(self.items) >= self.capacity

    def contains_item(self, item):
        return item in self.items