import json

def create_game_data(map_filename, state_filename):
    # Define initial state
    initial_state = {
        "characters": {
            "player": {
                "name": "PlayerName",
                "location": "Entrance",
                "inventory": []
            },
            "npc1": {
                "name": "Mysterious Wanderer",
                "location": "Hallway",
                "inventory": [],
                "behavior": "passive"
            }
        },
        "history": []
    }


    # Define game map
    game_map = {
    "Entrance": {
        "description": "You are at the entrance of the cave. {entrance_state} It's dark inside.",
        "dynamic_descriptions": {
            "entrance_state": {
                "default": "It's eerily quiet.",
                "after_visit": "The cave seems less intimidating now."
            }
        },
        "directions": {
            "north": "Hallway"
        },
        "state": {
            "visited": False
        }
    },
        "Hallway": {
            "description": "A narrow, damp hallway. You can see a light to the east. a {key} is on the floor. There is a {torch} on the wall.",
            "directions": {
                "south": "Entrance",
                "east": "Treasure Room",
                "west": "Trap Room"
            },
            "conditions": {},
            "interactive_items": [
                {
                    "name": "torch",
                    "description": "A torch hanging on the wall. It's currently unlit.",
                    "actions": ["pick_up"]
                },
                {
                    "name": "key",
                    "description": "A key. It looks like it could unlock something.",
                    "actions": ["pick_up", "inspect"]
                }
            ]
        },
        "Treasure Room": {
            "description": "A glittering room of treasures, but the exit north is locked.",
            "alternate_description": "The treasure room still sparkles, but you know the exit north is locked.",
            "directions": {
                "west": "Hallway",
                "north": "Secret Room"
            },
            "conditions": {
            }
        },
        "Trap Room": {
            "description": "A room with a suspicious floor. It's best not to linger.",
            "alternate_description": "The trap room. Watch your step.",
            "directions": {
                "east": "Hallway"
            },
            "conditions": {}
        },
        "Secret Room": {
            "description": "A mysterious room with an ancient artifact.",
            "alternate_description": "The secret room and its ancient artifact.",
            "directions": {
                "south": "Treasure Room"
            },
            "conditions": {}
        }
    }
    

    with open(map_filename, 'w') as f:
        json.dump(game_map, f, indent=4)

    with open(state_filename, 'w') as f:
        json.dump(initial_state, f, indent=4)

if __name__ == "__main__":
    create_game_data("game_data/game_map.json", "game_data/initial_state.json")