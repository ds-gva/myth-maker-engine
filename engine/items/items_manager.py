class ItemsManager:
    def __init__(self):
        self.items = {}

    def add_item(self, item):
        self.items[item.item_id] = item

    def remove_item(self, item_id):
        del self.items[item_id]

    def get_item(self, item_id):
        item = self.items.get(item_id)
        if not item:
            raise ValueError(f"No item with id {item_id}")
        return item

    def validate_item_actions(self, item, action_name):
        if action_name not in item.get_actions():
            raise ValueError(f"Invalid action {action_name} for item {item.id}")