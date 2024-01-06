from .character import Character

class Player(Character):
    def __init__(self, name, starting_location):
        super().__init__(name, starting_location)