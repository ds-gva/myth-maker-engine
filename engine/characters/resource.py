class Resource:
    def __init__(self, id, name, quantity=0):
        self.id = id
        self.name = name
        self.quantity = quantity

class ResourceInventory:
    def __init__(self):
        self.resources = {}

    def add_resource(self, resource):
        if resource.id in self.resources:
            self.resources[resource.id].quantity += resource.quantity
        else:
            self.resources[resource.id] = resource

    def update_resource_quantity(self, resource_id, quantity_change):
        if resource_id in self.resources:
            self.resources[resource_id].quantity += quantity_change
            return {"success": True, "message": f"You modified by {quantity_change} {self.resources[resource_id].id}."}
        else:
            return {"success": False, "message": f"Resource with ID {resource_id} not found in resources."}
        
    def remove_resource(self, resource_id, quantity):
        if resource_id in self.resources and self.resources[resource_id].quantity >= quantity:
            self.resources[resource_id].quantity -= quantity
            if self.resources[resource_id].quantity == 0:
                del self.resources[resource_id]
            return {"success": True, "message": f"Removed {quantity} of resource with ID {resource_id}."}
        else:
            return {"success": False, "message": f"Not enough of resource with ID {resource_id} in resources."}

    def get_all_resources(self):
        return self.resources.values()

    def get_resource_by_id(self, resource_id):
        return self.resources.get(resource_id)

    def has_resource(self, resource_id, quantity=1):
        return resource_id in self.resources and self.resources[resource_id].quantity >= quantity