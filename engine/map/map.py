class Map:
    def __init__(self, rooms, items_manager):
        self.rooms = rooms
        self.items_manager = items_manager

    def get_items_manager(self):
        return self.items_manager

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
    