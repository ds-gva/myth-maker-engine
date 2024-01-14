from .character import Character
from engine.dialogues.dialogue import Dialogue

class NPC(Character):
    def __init__(self, name, starting_location, id, dialogue_id, dialogue_starting_node_id='START'):
        super().__init__(name, starting_location)
        self.id = id
        self.name = name
        self.dialogue_id = dialogue_id
        self.dialogue_starting_node_id = dialogue_starting_node_id