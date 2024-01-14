class Action:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def execute(self, game, character, context=None):
        raise NotImplementedError("Execute method must be implemented by subclasses.")
    
class CustomAction(Action):
    def __init__(self, name, description, func):
        super().__init__(name, description)
        self.func = func

    def execute(self, game, character, context=None):
        return self.func(game, character, context)

class ActionRegistry:
    def __init__(self):
        self.actions = {}

    def register_action(self, action):
        if action.name in self.actions:
            raise ValueError(f"Action {action.name} is already registered.")
        self.actions[action.name] = action

    def get_action(self, action_name):
        return self.actions.get(action_name)

    def execute_action(self, action_name, game, character, context=None):
        action = self.get_action(action_name)
        if not action:
            raise ValueError(f"Action {action_name} not found.")
        return action.execute(game, character, context)
    
