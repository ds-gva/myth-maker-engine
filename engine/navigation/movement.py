class Movement:
        def __init__(self, game_map):
            self.game_map = game_map

        def move(self, character, direction, target_room_id):
            if not self.can_move(character.location, direction, target_room_id):
                return None
            return self.perform_move(character, direction, target_room_id)

        def perform_move(self, character, direction, target_room_id):
            new_location = self.get_new_location(target_room_id).id
            character.location = new_location
            character.history.append({'direction': direction, 'location': new_location})
            return new_location

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