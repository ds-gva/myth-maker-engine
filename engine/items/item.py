from engine.items.item_actions import ItemActions
    
class Item:
    def __init__(self, name, item_id, description, owner=None, actions=None, stackable=False, quantity=1, droppable=True):
        self.name = name
        self.item_id = item_id
        self.description = description
        self.owner = owner
        self.actions = actions
        self.action_functions = {action_name: ItemActions.actions.get(action_name) for action_name in actions if ItemActions.actions.get(action_name)} if actions else {}
        self.stackable = stackable
        self.quantity = quantity
        self.droppable = droppable
        self.dropped = False

    def inspect(self):
        return self.name, self.description, self.get_actions(only_room=True)

    def interact(self, game, character, action_name):
        if not self.actions:
            return self.description
        action_result = ItemActions.perform_action(action_name, game, character, self)
        if action_result['success']:
            self.handle_consequence(game, character, action_name)
        return action_result

    def handle_consequence(self, game, character, action_name):
        action = self.actions[action_name]
        if 'consequence' in action and action['consequence'] == 'set_state':
            self.set_state(game, character, action)

    def set_state(self, game, character, action):
        room = game.map.get_room_by_id(character.location)
        state_to_change = action['state_change']
        for key, value in state_to_change.items():
            room.state[key] = value

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
            'actions': self.actions,
            'stackable' : self.stackable,
            'quantity': self.quantity,
            'droppable': self.droppable,
            'dropped': self.dropped
        }