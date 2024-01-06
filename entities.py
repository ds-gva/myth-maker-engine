class Room:
    def __init__(self, name, room_id, base_description, directions, conditions, dynamic_text, state, interactive_items, npcs):
        self.name = name
        self.id = room_id
        self.base_description = base_description
        self.directions = directions
        self.conditions = conditions or {}
        self.dynamic_text = dynamic_text or {}
        self.state = state or {}
        self.interactive_items = interactive_items
        self.npcs = npcs
        self.dropped_items = {}
        
    def get_description(self):
        description = self.base_description
        for key, dynamic_text in self.dynamic_text.items():
            placeholder = '{' + key + '}'
            text = dynamic_text['default']
            for condition, condition_text in dynamic_text['conditions'].items():
                if self.state.get(condition) == 'true':
                    text = condition_text
                    break
            description = description.replace(placeholder, text)
        return description

    def get_parsed_description(self):
        parsed_description = self.get_description()
        interactive_items_data = {}
        for item_id, item in self.interactive_items.items():
            interactive_items_data[item_id] = {
                'name': item.name,
                'description': item.description
            }

        npcs_data = {}
        for npc_id, npc in self.npcs.items():
            npcs_data[npc_id] = {
                'name': npc.name
            }
        
        dropped_items_data = {}
        for item_id, item in self.dropped_items.items():
            dropped_items_data[item_id] = {
                'name': item.name,
            }

        return parsed_description, interactive_items_data, npcs_data, dropped_items_data
        
    def get_interactive_items(self):
        return self.interactive_items

    def set_description(self, description):
        self.description = description

    def get_dropped_items(self):
        return self.dropped_items

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

class Character:
    def __init__(self, name, starting_location):
        self.name = name
        self.location = starting_location
        self.history = [{'direction': 'START', 'location': starting_location}]
        self.inventory = Inventory(10)

    def add_to_inventory(self, item):
        return self.inventory.add_item(item)

    def remove_from_inventory(self, item):
        self.inventory.remove_item(item)

    def get_inventory(self, as_dict=False):
        if not as_dict:
            return self.inventory.get_capacity(), self.inventory
        else:
            return self.inventory.get_capacity(), [item.to_dict() for item in self.inventory.get_items()]

class Player(Character):
    def __init__(self, name, starting_location):
        super().__init__(name, starting_location)
        # Additional player-specific initialization

class NPC(Character):
    def __init__(self, name, starting_location, behavior=None):
        super().__init__(name, starting_location)

        
class ItemActions:
    @staticmethod
    def pick_up(game, character, item):
        if character.add_to_inventory(item):
            item.owner = character
            room = game.map.get_room_by_id(character.location)
            if item.dropped:
                del room.dropped_items[item.item_id]
                item.dropped = False
            else:
                del room.interactive_items[item.item_id]
        else:
            return "You can't carry any more items."
        
    @staticmethod
    def drop(game, character, item):
        character.remove_from_inventory(item)
        room = game.map.get_room_by_id(character.location)
        item.owner = room
        item.dropped = True
        room.dropped_items[item.item_id] = item
        return f"You dropped the {item.name}."
    
class Item:
    ACTIONS = {
        'pick_up': ItemActions.pick_up,
        'drop': ItemActions.drop,
        # Add more actions here
    }

    def __init__(self, name, item_id, description, owner=None, actions=None):
        self.name = name
        self.item_id = item_id
        self.description = description
        self.owner = owner
        self.actions = actions
        self.action_functions = {action_name: self.ACTIONS.get(action_name) for action_name in actions if self.ACTIONS.get(action_name)} if actions else {}
        self.dropped = False

    def interact(self, game, character, action_name):
        if not self.actions:
            return self.description

        action_result = self.perform_action(game, character, action_name)
        self.handle_consequence(game, character, action_name)

        return action_result

    def perform_action(self, game, character, action_name):
        return self.action_functions[action_name](game, character, self)

    def handle_consequence(self, game, character, action_name):
        action = self.actions[action_name]
        if 'consequence' in action and action['consequence'] == 'set_state':
            self.set_state(game, character, action)

    def set_state(self, game, character, action):
        room = game.map.get_room_by_id(character.location)
        state_to_change = action['state_change']
        for key, value in state_to_change.items():
            room.state[key] = value

    def inspect(self):
        return self.name, self.description, self.get_actions(only_room=True)

    def get_actions(self, only_room=False):
        if only_room:
            return [key for key, value in self.actions.items() if value.get('visible_in_room') == 'true']
        else:
            return list(self.actions.keys())

    def to_dict(self):
        return {
            'name': self.name,
            'item_id': self.item_id,
            'description': self.description,
            'owner': self.owner,
            'actions': self.actions
        }
    
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