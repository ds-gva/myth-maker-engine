class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        if len(self.items) < self.capacity:
            if item.stackable and self.contains_item_by_id(item.item_id):
                existing_item = self.get_item_by_id(item.item_id)
                existing_item.quantity += item.quantity
            else:
                self.items.append(item)
            return True
        else:
            return False  # Inventory is full

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        else:
            return False

    def get_items(self):
        return self.items
    
    def get_capacity(self):
        return self.capacity

    def is_full(self):
        return len(self.items) >= self.capacity

    def contains_item(self, item):
        return item in self.items
    
    def contains_item_by_id(self, item_id):
        return any(item.item_id == item_id for item in self.items)