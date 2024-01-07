import json
from .map.map import Map
from .map.map_loader import MapLoader
from .characters.player import Player
from .navigation.movement import Movement
from .characters.resource import Resource

class Game:
    def __init__(self, initial_state_data, game_map_data, game_dialogues_data):
        self.state = {}
        self.characters = {}
        self.map_loader = MapLoader(game_map_data)
        self.rooms, self.items_manager = self.map_loader.load()
        self.map = Map(self.rooms, self.items_manager)
        self.movement = Movement(self.map)
        self.items_manager = self.map.get_items_manager()
        self.dialogues = self.load_dialogues(game_dialogues_data)
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
        if not character:
            raise ValueError(f"No character with name {character_name}")
        new_location = self.movement.move(character, direction, target_room_id)
        if not new_location:
            raise ValueError("You can't go that way.")
        return new_location
    
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
    
    def load_dialogues(self, game_dialogues_data):
        with open(game_dialogues_data, 'r') as f:
            dialogues_data = json.load(f)
        return dialogues_data