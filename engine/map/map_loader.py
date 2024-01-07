from engine.rooms.room import Room
from engine.items.item import Item
from engine.characters.npc import NPC
from engine.items.items_manager import ItemsManager
import json

class MapLoader:
    def __init__(self, game_map_data):
        self.game_map_data = game_map_data
        self.items_manager = ItemsManager()

    def load(self):
        with open(self.game_map_data, 'r') as f:
            game_map = json.load(f)
            rooms = {}
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
                rooms[room.id] = room
            return rooms, self.items_manager

    def load_interactive_items(self, room_data, room_name):
        interactive_items = {}
        for item_name, item_data in room_data.get('interactive_items', {}).items():
            item_id = item_data['id']
            item_droppable = item_data.get('droppable', 'true').lower() == 'true'
            item = Item(item_name, item_id, item_data['description'], room_name, item_data['actions'], droppable=item_droppable)
            interactive_items[item_id] = item
            self.items_manager.add_item(item)
        return interactive_items
    
    def load_npcs(self, room_data):
        npcs = {}
        for npc_name, npc_data in room_data.get('npcs', {}).items():
            npc_id = npc_data['id']
            npc_name = npc_data['name']
            interact_trigger = npc_data['interact_trigger']
            npc = NPC(npc_name, room_data['id'], npc_id, interact_trigger)
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
