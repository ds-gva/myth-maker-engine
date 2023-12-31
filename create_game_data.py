import json

def create_game():
    # Define initial state
    initial_state = {
        'location': 'Hoth',
        'history': []
    }

    # Define game map
    map = {
    "Tatooine": {
        "north": "Death Star",
        "east": "Hoth",
        "description": "You are on Tatooine, a harsh desert world."
    },
    "Death Star": {
        "south": "Tatooine",
        "east": "Endor",
        "description": "You are on the Death Star, a moon-sized military battlestation."
    },
    "Hoth": {
        "west": "Tatooine",
        "north": "Endor",
        "description": "You are on Hoth, a remote icy planet."
    },
    "Endor": {
        "south": "Hoth",
        "west": "Death Star",
        "description": "You are on Endor, a forested moon."
    }
    }
    

    # Save initial state and map to JSON files
    with open('game_data/initial_state.json', 'w') as f:
        json.dump(initial_state, f)
    with open('game_data/game_map.json', 'w') as f:
        json.dump(map, f)

if __name__ == '__main__':
    create_game()