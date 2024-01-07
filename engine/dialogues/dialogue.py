class Dialogue:
    def __init__(self, dialogue_data):
        self.dialogue_data = dialogue_data
        self.current_node = dialogue_data['nodes'][0]

    def get_current_line(self):
        return self.current_node['text']

    def get_player_responses(self):
        return [choice['text'] for choice in self.current_node['choices']]

    def choose_response(self, response_index):
        self.current_node = self.dialogue_data['nodes'][self.current_node['choices'][response_index]['next_node']]   