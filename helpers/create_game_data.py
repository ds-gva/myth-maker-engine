import json

def create_game_data(map_filename, state_filename, dialogues_filename):
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

    dialogues = {

    "dialogue_id": "npc_mother_dialogue",
    "nodes": [
                {
                    "id": "greeting",
                    "text": "Hello, adventurer!",
                    "choices": [
                        {
                            "text": "Hello!",
                            "next_node": "question1",
                            "conditions": {}
                        },
                        {
                            "text": "Goodbye.",
                            "next_node": 'None',
                            "conditions": {}
                        }
                    ]
                },
                {
                    "id": "question1",
                    "text": "Can you help me find my lost item?",
                    "choices": [
                        {
                            "text": "Yes, I can help.",
                            "next_node": "thanks",
                            "conditions": {}
                        },
                        {
                            "text": "No, I can't help.",
                            "next_node": "goodbye",
                            "conditions": {}
                        }
                    ]
                }
            ]
    }   

    # Define game map
    game_map = {
        "Home": {
            "id": "home",
            "base_description": "You are at home with your [mother1] and sister. The house is warm and cozy. At the north of the room there is a door to go outside, it's unlocked. {scarf1_description}. {coins_description}",
            "dynamic_text": {
                "scarf1_description": {
                    "default": "A [scarf1] is folded on a chair by the door",
                    "conditions": [
                        {
                            "condition": "scarf1_taken",
                            "text": "The chair by the door is empty."
                        }
                    ]
                    },
                "coins_description": {
                    "default": "There are [resource: coins | 10 | coins | coins1_taken] on the table.",
                    "conditions": [
                        {
                            "condition": "coins1_taken",
                            "text": "There is nothing on the table."
                        }
                    ]
                    },
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
                "scarf1_taken": 'false',
                "coins1_taken": 'false'
            },
            "npcs": {
                "mother": {
                    "id": "mother1",
                    "name": "Mother",
                    "interact_trigger": "npc_mother_dialogue",
                    }
            },
            "interactive_items": {
                "scarf": {
                    "id": "scarf1",
                    "description": "It's a nice warm woolen scarf. Very useful on cold nights.",
                    "droppable": 'false',
                    "actions": {
                        "pick_up": {
                            "consequence": "set_state",
                            "state_change": {
                                "scarf1_taken": 'true'
                            },
                            "visible_in_room": "true"
                        },
                        "drop": {
                            "visible_in_room": "false"
                        }
                    },
                    "conditions": {
                        "scarf1_taken": 'false'
                    }
                }
            },
        },
        "Outside": {
            "id": "outside1",
            "base_description": "You step outside. It's a cold, clear night. The stars are shining brightly. There is a small shed to the east. {tree1_description}",
            "dynamic_text": {
                "tree1_description": {
                    "default": "There is a patch of [tree1] in the corner of the garden.",
                "conditions": [
                    {
                        "condition": "trees_chopped",
                        "text": "There is a pile of [resource: wood | 10 | chopped wood | wood_taken] in the corner of the garden."
                    },
                    {
                        "condition": "wood_taken",
                        "text": "A few stubs of wood in the corner of the garden."
                    }
                ]
                }
            },

            "directions": {
                "south": {
                    "direction_id": "home"
                },
                "east": {
                    "direction_id": "shed1"
                }
            },
            "state": {
                "trees_chopped": "false",
                "wood_taken": "false"
            },
            "interactive_items": {
                "fir trees": {
                    "id": "tree1",
                    "description": "A patch of fir-trees, about my height.",
                    "actions": {
                        "chop_trees": {
                            "consequence": "set_state",
                                "state_change": {
                                    "trees_chopped": 'true'
                                },
                            "visible_in_room": "true"
                        },
                    }
                }
                
            }
        },
        "Shed": {
                "id": "shed1",
                "base_description": "You are in a small shed. It's dark and dusty, with tools scattered around. {axe1_description}",
                "dynamic_text": {
                    "axe1_description": {
                        "default": "I can see an [axe1].",
                    "conditions": [
                    {
                        "condition": "axe_taken",
                        "text": "Most of these tools are too old to be used."
                    }
                    ]
                    }
                },
                "directions": {
                    "west": {
                        "direction_id": "outside1"
                    }
                },
                "state": {
                    "axe_taken": "false",
                },
                "npcs": {},
                "interactive_items": {
                      "axe": {
                        "id": "axe1",
                        "description": "It's a rusty axe, helpful for chopping wood.",
                        "actions": {
                            "pick_up": {
                                "consequence": "set_state",
                                "state_change": {
                                    "axe_taken": 'true',
                                },
                                "visible_in_room": "true"
                            },
                            "drop": {
                            "visible_in_room": "false"
                            }
                        },
                        "conditions": {
                            "axe_taken": "false"
                        }
                      }
                }
            }
      }

    with open(map_filename, 'w') as f:
        json.dump(game_map, f, indent=4)

    with open(state_filename, 'w') as f:
        json.dump(initial_state, f, indent=4)
    
    with open(dialogues_filename, 'w') as f:
        json.dump(dialogues, f, indent=4)

if __name__ == "__main__":
    create_game_data("./game_data/game_map.json", "./game_data/initial_state.json", "game_data/dialogues.json")