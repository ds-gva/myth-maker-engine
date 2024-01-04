import json

def create_game_data(map_filename, state_filename):
    # Define initial state
    initial_state = {
        "characters": {
            "player": {
                "name": "PlayerName",
                "location": "home",
                "inventory": []
            }
        },
        "history": []
    }


    # Define game map
    game_map = {
        "Home": {
            "id": "home",
            "base_description": "You are at home with your mother and sister. The house is warm and cozy. At the north of the room there is a door to go outside, it's unlocked. {scarf1_description}.",
            "dynamic_text": {
                "scarf1_description": {
                    "default": "A [scarf1] is folded on a chair by the door",
                    "conditions": {
                        "scarf1_taken": "The chair by the door is empty"
                    }
                }
            },
            "directions": {
                "north": {
                    "direction_id": "outside1",
                    "conditions": {
                        "scarf1_taken": 'true'
                    }
                }
            },
            "state": {
                "scarf1_taken": 'false'
            },
            "interactive_items": {
                "scarf": {
                    "id": "scarf1",
                    "description": "It's a nice warm woolen scarf. Very useful on cold nights.",
                    "actions": {
                        "pick_up": {
                            "consequence": "set_state",
                            "state_change": {
                                "scarf1_taken": 'true'
                            }
                        }
                    },
                    "conditions": {
                        "scarf1_taken": 'false'
                    }
                }
            }
        },
        "Outside": {
            "id": "outside1",
            "base_description": "You step outside. It's a cold, clear night. The stars are shining brightly. There is a small shed to the east.",
            "dynamic_text": {},
            "directions": {
                "south": {
                    "direction_id": "home"
                },
                "east": {
                    "direction_id": "shed1"
                }
            },
            "state": {},
            "interactive_items": {}
        },
        "Shed": {
                "id": "shed1",
                "base_description": "You are in a small shed. It's dark and dusty, with tools scattered around. {hammer1_description}.",
                "dynamic_text": {
                    "hammer1_description": {
                        "default": "I can't see much.",
                        "conditions": {
                            "light_on": "I can see a [hammer1].",
                            "light_on_hammer_taken": "These other tools aren't really useful.",
                        }
                    }
                },
                "directions": {
                    "west": {
                        "direction_id": "outside1"
                    }
                },
                "state": {
                    "light_on": "true",
                    "light_on_hammer_taken": "false"
                },
                "interactive_items": {
                      "hammer": {
                        "id": "hammer1",
                        "description": "It's a heavy hammer.",
                        "actions": {
                            "pick_up": {
                                "consequence": "set_state",
                                "state_change": {
                                    "light_on_hammer_taken": 'true',
                                    "light_on": "false"
                                }
                            }
                        },
                        "conditions": {
                            "light_on": "true"
                        }
                      }
                }
            }
      }

    with open(map_filename, 'w') as f:
        json.dump(game_map, f, indent=4)

    with open(state_filename, 'w') as f:
        json.dump(initial_state, f, indent=4)

if __name__ == "__main__":
    create_game_data("game_data/game_map.json", "game_data/initial_state.json")