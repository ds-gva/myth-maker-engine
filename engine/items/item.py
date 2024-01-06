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