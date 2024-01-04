import json
from entities import Room, Player
from entities import Item, ItemActions, ItemsManager

class Game:
    def __init__(self, initial_state_data, game_map_data):
        self.state = {}
        self.characters = {}
        self.map = Map(game_map_data)
        self.movement = Movement(self.map)
        self.items_manager = self.map.get_items_manager()
        self.load_initial_state(initial_state_data)

    def load_initial_state(self, initial_state_data):
        with open(initial_state_data, 'r') as f:
            initial_state = json.load(f)
            for character_data in initial_state['characters'].values():
                character = Player(character_data['name'], character_data['location'])
                self.add_character(character)
            self.state['history'] = initial_state['history']

    def add_character(self, character):
        self.characters[character.name] = character
        if isinstance(character, Player):
            self.state['player_name'] = character.name  # Track the player's character name

    def get_character(self, character_name):
        return self.characters.get(character_name)

    def move_character(self, character_name, direction, target_room_id):
        character = self.get_character(character_name)
        if character:
            new_location = self.movement.get_new_location(target_room_id)
            if new_location:
                return self.movement.move(character, direction, target_room_id)
            else:
                return "You can't go that way."
    
    def inspect_item(self, item_id):
        item = self.items_manager.get_item(item_id) 
        if item:
            item_name, item_description, item_actions = item.inspect()
            return item_name, item_description, item_actions
        return "You can't inspect that.", []

    def interact_with_item(self, character_name, item_id, action_name):
        character = self.get_character(character_name)
        if character:
            print("1")
            item = self.items_manager.get_item(item_id)
            print(item)
            if item and action_name in item.get_actions():
                print(item.get_actions())
                return item.interact(self, character, action_name)
        return "You can't interact with that."


class Map:
    def __init__(self, game_map_data):
        self.rooms = {}
        self.items_manager = ItemsManager()
        self.load_map(game_map_data)
    
    def get_items_manager(self):
        return self.items_manager

    def load_map(self, game_map_data):
        with open(game_map_data, 'r') as f:
            game_map = json.load(f)
            for room_name, room_data in game_map.items():
                interactive_items = {}
                for item_name, item_data in room_data['interactive_items'].items():
                    item_id = item_data['id']
                    item = Item(item_name, item_id, item_data['description'], room_name, item_data['actions'])
                    interactive_items[item_id] = item
                    self.items_manager.add_item(item)

                directions = {}
                for direction, direction_data in room_data['directions'].items():
                    if isinstance(direction_data, dict):
                        directions[direction] = direction_data
                    else:
                        directions[direction] = {'id': direction_data}
                room = Room(room_name,
                            room_data['id'],
                            room_data['base_description'],
                            directions,
                            room_data.get('conditions'),
                            room_data.get('dynamic_text'),
                            room_data.get('state'),
                            interactive_items)
                self.rooms[room.name] = room

    def get_room_by_id(self, room_id):
        for room in self.rooms.values():
            if room.id == room_id:
                return room
        return None

    def can_move(self, current_room, direction):
        room = self.get_room_by_id(current_room)
        return direction in room.directions

    def meets_conditions(self, current_room, direction, state):
        room = self.get_room_by_id(current_room)
        condition = room.conditions.get(direction)
        return condition is None or condition in state.get('inventory', [])

    def get_new_location(self, current_room, direction):
        return self.rooms[current_room].directions[direction]
    
class Movement:
        def __init__(self, game_map):
            self.game_map = game_map

        def move(self, character, direction, target_room_id):
            current_location = character.location
            print(current_location)
            if self.can_move(current_location, direction, target_room_id):
                print(f'Moving {character.name} {target_room_id}')
                new_location = self.get_new_location(target_room_id).id
                character.location = new_location
                character.history.append({'direction': direction, 'location': new_location})
                return new_location
            else:
                return None

        def can_move(self, current_location, direction, target_room_id):
            if not self.game_map.can_move(current_location, direction):
                return False
            room = self.game_map.get_room_by_id(current_location)
            direction_data = room.directions[direction]
            if 'conditions' in direction_data:
                for condition, required_value in direction_data['conditions'].items():
                    if room.state.get(condition) != required_value:
                        return False
            return True

        def get_new_location(self, target_room_id):
            return self.game_map.get_room_by_id(target_room_id)