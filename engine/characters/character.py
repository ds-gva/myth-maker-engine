from .inventory import Inventory
from .resource import Resource, ResourceInventory

class Character:
    def __init__(self, name, starting_location):
        self.name = name
        self.location = starting_location
        self.history = [{'direction': 'START', 'location': starting_location}]
        self.inventory = Inventory(10)
        self.resources = ResourceInventory()

    def add_to_inventory(self, item):
        return self.inventory.add_item(item)

    def remove_from_inventory(self, item):
        self.inventory.remove_item(item)

    def get_inventory(self, get_capacity=True, as_dict=False):
        if not as_dict:
            if get_capacity:
                return self.inventory.get_capacity(), self.inventory
            else:
                return self.inventory
        else:
            if get_capacity:
                return self.inventory.get_capacity(), [item.to_dict() for item in self.inventory.get_items()]
            else:
                [item.to_dict() for item in self.inventory.get_items()]