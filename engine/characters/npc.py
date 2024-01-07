from .character import Character
from engine.dialogues.dialogue import Dialogue

class NPC(Character):
    def __init__(self, name, starting_location, id, interact_trigger):
        super().__init__(name, starting_location)
        self.name = name
        self.id = id
        self.interact_trigger = interact_trigger
        self.dialogue = None

    def get_interact_trigger(self):
        return self.interact_trigger
    
    def start_dialogue(self, dialogue_data):
        self.dialogue = Dialogue(dialogue_data)