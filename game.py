import json

from entities import Room

class Game:
    def __init__(self, initial_state_data, game_map_data):
        self.state = {}
        self.map = {}
        self.load_initial_state(initial_state_data, game_map_data)

    def load_initial_state(self, initial_state_data, game_map_data):
        with open(initial_state_data, 'r') as f:
            self.state.update(json.load(f))
        with open(game_map_data, 'r') as f:
            game_map = json.load(f)
            for room_name, room_data in game_map.items():
                self.map[room_name] = Room(room_name, room_data['description'], {direction: location for direction, location in room_data.items() if direction != 'description'})

    def move(self, direction):
        current_location = self.state['location']
        if direction in self.map[current_location].directions:
            self.state['location'] = self.map[current_location].directions[direction]
            self.state['history'].append({'direction': direction, 'location': self.state['location']})
            return self.map[self.state['location']].description
        else:
            return "You can't go that way."
    
    def save_state(self):
        with open('game_state.json', 'w') as f:
            json.dump(self.state, f)

    def load_state(self):
        with open('game_state.json', 'r') as f:
            self.state.update(json.load(f))