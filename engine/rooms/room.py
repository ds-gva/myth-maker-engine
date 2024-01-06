import re

class Room:
    def __init__(self, name, room_id, base_description, directions, conditions, dynamic_text, state, interactive_items, npcs):
        self.name = name
        self.id = room_id
        self.base_description = base_description
        self.directions = directions
        self.conditions = conditions or {}
        self.dynamic_text = dynamic_text or {}
        self.state = state or {}
        self.interactive_items = interactive_items
        self.npcs = npcs
        self.dropped_items = {}
        
    def get_description(self):
        description = self.base_description
        for key, dynamic_text in self.dynamic_text.items():
            placeholder = '{' + key + '}'
            text = dynamic_text['default']
            for condition, condition_text in dynamic_text['conditions'].items():
                if self.state.get(condition) == 'true':
                    text = condition_text
                    break
            description = description.replace(placeholder, text)

        return description

    def get_parsed_description(self):
        parsed_description = self.get_description()

        interactive_items_data = {}
        for item_id, item in self.interactive_items.items():
            interactive_items_data[item_id] = {
                'name': item.name,
                'description': item.description
            }

        npcs_data = {}
        for npc_id, npc in self.npcs.items():
            npcs_data[npc_id] = {
                'name': npc.name
            }
        
        dropped_items_data = {}
        for item_id, item in self.dropped_items.items():
            dropped_items_data[item_id] = {
                'name': item.name,
            }

        resources_data = {}
        resource_tags = re.findall(r'\[resource: .+?]', parsed_description)
        for tag in resource_tags:
            _, resource_id, resource_quantity, resource_text, resource_state_change = re.split(r': |\| ', tag.strip('[]'))
            resource_quantity = int(resource_quantity)

            resources_data[resource_id] = {
                'quantity': resource_quantity,
                'text': resource_text,
                'state_change': resource_state_change
            }

        return parsed_description, interactive_items_data, npcs_data, dropped_items_data, resources_data
        
    def get_interactive_items(self):
        return self.interactive_items

    def set_description(self, description):
        self.description = description

    def get_dropped_items(self):
        return self.dropped_items
    
    def room_resource_state_change(self, resource_state_change):
        self.state[resource_state_change] = 'true'
        print(self.state['coins1_taken'])
