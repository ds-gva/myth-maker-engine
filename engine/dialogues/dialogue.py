class Dialogue:
    def __init__(self, dialogue_data):
        self.dialogue_data = dialogue_data
        self.current_node = self.get_node_by_id(self.dialogue_data['start_node_id'])

    def get_node_by_id(self, node_id):
        for node in self.dialogue_data['nodes']:
            if node['id'] == node_id:
                return node
        raise ValueError(f"No node with id {node_id}")

class DialogueManager:
    def __init__(self, dialogues_data):
        self.dialogues_data = dialogues_data
        self.dialogues = {}
        self.active_dialogues = {}
        self.load_dialogues()

# parse the dialogues_data to load all the dialogues
    def load_dialogues(self):
        for dialogue_data in self.dialogues_data:
            self.dialogues[dialogue_data['dialogue_id']] = Dialogue(dialogue_data)

# add a dialogue outside of the initially loaded dialogues
    def add_dialogue(self, dialogue):
        self.dialogues[dialogue.dialogue_id] = dialogue

    def get_dialogue_by_id(self, dialogue_id):
        dialogue = self.dialogues.get(dialogue_id)
        if not dialogue:
            raise ValueError(f"No dialogue with id {dialogue_id}")
        return dialogue
    
    # get dialogue node by id ; inputs are dialogue_id and starting_node_id
    # raise error if node_id does not exist
    
    def start_dialogue(self, dialogue_id, starting_node_id='START'):
        dialogue = self.get_dialogue_by_id(dialogue_id)
        active_dialogue = Dialogue(dialogue.dialogue_data)    # Create a new Dialogue object for the active dialogue
        # If the starting_node_id is not the default, set the current_node to the starting_node_id
        self.active_dialogues[dialogue_id] = active_dialogue  # Store the active dialogue
        if starting_node_id != 'START':
            self.active_dialogues[dialogue_id].current_node = active_dialogue.get_node_by_id(starting_node_id)         

        return dialogue_id, self.active_dialogues[dialogue_id].current_node

    def proceed_dialogue(self, dialogue_id, choice_id):
        self.active_dialogues[dialogue_id].current_node = self.active_dialogues[dialogue_id].get_node_by_id(choice_id)
        next_node = self.active_dialogues[dialogue_id].current_node 
        if not next_node:
            del self.active_dialogues[dialogue_id]
            return {"end": True, "message": "Dialogue ended"}
        return dialogue_id, next_node