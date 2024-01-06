import json
from entities import Room, Player, NPC
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
        item_name, item_description, item_actions = item.inspect()
        return item_name, item_description, item_actions

    def interact_with_item(self, character_name, item_id, action_name):
        character = self.get_character(character_name)
        if not character:
            raise ValueError(f"No character with name {character_name}")
        item = self.items_manager.get_item(item_id)
        self.items_manager.validate_item_actions(item, action_name)
        return item.interact(self, character, action_name)


class Map:
    def __init__(self, game_map_data):
        self.rooms = {}
        self.items_manager = ItemsManager()
        self.load_map(game_map_data)
    
    def get_items_manager(self):
        return self.items_manager

    def load_interactive_items(self, room_data, room_name):
        interactive_items = {}
        for item_name, item_data in room_data.get('interactive_items', {}).items():
            item_id = item_data['id']
            item = Item(item_name, item_id, item_data['description'], room_name, item_data['actions'])
            interactive_items[item_id] = item
            self.items_manager.add_item(item)
        return interactive_items
    
    def load_npcs(self, room_data):
        npcs = {}
        for npc_name, npc_data in room_data.get('npcs', {}).items():
            npc_id = npc_data['id']
            npc = NPC(npc_name, npc_id, npc_data['name'])
            npcs[npc_id] = npc
        return npcs
    
    def load_directions(self, room_data):
        directions = {}
        for direction, direction_data in room_data.get('directions', {}).items():
            if isinstance(direction_data, dict):
                directions[direction] = direction_data
            else:
                directions[direction] = {'id': direction_data}
        return directions

    def load_map(self, game_map_data):
        with open(game_map_data, 'r') as f:
            game_map = json.load(f)
            for room_name, room_data in game_map.items():
                interactive_items = self.load_interactive_items(room_data, room_name)
                npcs = self.load_npcs(room_data)
                directions = self.load_directions(room_data)
                room = Room(room_name,
                            room_data['id'],
                            room_data['base_description'],
                            directions,
                            room_data.get('conditions'),
                            room_data.get('dynamic_text'),
                            room_data.get('state'),
                            interactive_items,
                            npcs)
                self.rooms[room.id] = room
    
    def get_room_by_id(self, room_id):
        room = self.rooms.get(room_id)
        print(room)
        if not room:
            raise ValueError(f"No room with id {room_id}")
        return room

    def can_move(self, current_room, direction):
        room = self.get_room_by_id(current_room)
        return direction in room.directions

    def meets_conditions(self, current_room, direction, state):
        room = self.get_room_by_id(current_room)
        condition = room.conditions.get(direction)
        return condition is None or condition in state.get('inventory', [])

    def get_new_location(self, current_room, direction):
        room = self.get_room_by_id(current_room)
        return room.directions[direction]
    
class Movement:
        def __init__(self, game_map):
            self.game_map = game_map

        def move(self, character, direction, target_room_id):
            current_location = character.location
            if self.can_move(current_location, direction, target_room_id):
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