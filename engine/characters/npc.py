from .character import Character

class NPC(Character):
    def __init__(self, name, starting_location, behavior=None):
        super().__init__(name, starting_location)