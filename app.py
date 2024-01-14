from flask import Flask, request, render_template, jsonify
from engine.game import Game
from engine.items.item_actions import ItemActions
from engine.characters.resource import Resource
from engine.dialogues.dialogue import DialogueManager
from engine.actions.action import CustomAction
from engine.actions.action import ActionRegistry


app = Flask(__name__)

GAME_TITLE = "TestGame"
PLAYER_NAME = 'PlayerName'

INITIAL_STATE_FILE = 'game_data/initial_state.json'
GAME_MAP_FILE = 'game_data/game_map.json'
GAME_DIALOGUES_FILE = 'game_data/dialogues.json'
GAME_RESOURCES_FILE = 'game_data/resources.json'


game = Game(GAME_TITLE, INITIAL_STATE_FILE, GAME_MAP_FILE, GAME_DIALOGUES_FILE, GAME_RESOURCES_FILE)
player = game.get_character(PLAYER_NAME)
game.populate_resources(PLAYER_NAME)

# Define a new action attached to an item
def chop_trees(game, character, item):
    player_inventory = character.get_inventory(get_capacity=False)
    if player_inventory.contains_item_by_id('axe1'):
        return {"success": True, "message": "You successfully chopped the trees."}
    else:
        return {"success": False, "message": "You need an axe to chop the trees."}

ItemActions.register_action("chop_trees", chop_trees)


# Define a new general action (which can be called e.g., in a dialogue)
def change_npc_dialogue(game, character, context=None):
    npc_id, dialogue_id = context.split()
    npc = game.map.get_room_by_id(character.location).get_npcs_by_id(npc_id)
    npc.dialogue_id = dialogue_id
    print(npc_id, dialogue_id)
    # rest of the function

change_npc_dialogue_action = CustomAction("change_npc_dialogue", "Changes an NPCs dialgoue.", change_npc_dialogue)
action_registry = ActionRegistry()
action_registry.register_action(change_npc_dialogue_action)


@app.route('/', methods=['GET', 'POST'])
def game_route():
    description = None
    interactive_items = None
    current_location = player.location
    current_room = game.map.get_room_by_id(current_location)

    if request.method == 'POST':
        direction = request.form.get('direction')
        target_room_id = current_room.directions[direction]['direction_id']
        if game.movement.can_move(player.location, direction, target_room_id):
            game.move_character(player.name, direction, target_room_id)
            current_room = game.map.get_room_by_id(target_room_id)
        else:
            print("You can't go that way.")

    description = current_room.get_parsed_description()
    directions = current_room.directions

    return render_template('game.html',
                            game_title=game.title,
                            room_name=current_room.name,
                            room_id=current_room.id,
                            description=description,
                            directions=directions,
                            history=player.history,
                            interactive_items=interactive_items)

@app.route('/get_room_description/<room_id>', methods=['POST'])
def get_room_description_route(room_id):
    current_room = game.map.get_room_by_id(room_id)
    description, interactive_items_data, npcs_data, dropped_items_data, resources_data = current_room.get_parsed_description()

    return jsonify(description=description, interactive_items=interactive_items_data, npcs=npcs_data, dropped_items=dropped_items_data, resources_data=resources_data)

@app.route('/inspect_item/<item_id>', methods=['POST'])
def inspect_route(item_id):
    item_name, item_description, item_actions = game.inspect_item(item_id)
    return jsonify(item_name=item_name, item_description=item_description, item_actions=item_actions)

@app.route('/interact_with_item/<item_id>/<action_name>', methods=['POST'])
def interact_route(item_id, action_name):
    result = game.interact_with_item(player.name, item_id, action_name)
    return jsonify(result=result)

@app.route('/inventory', methods=['GET'])
def inventory_route():
    inventory_capacity, inventory = player.get_inventory()
    inventory_list = [{'name': item.name, 'item_id': item.item_id, 'quantity': item.quantity} for item in inventory.items]
    return jsonify(inventory_capacity=inventory_capacity, inventory=inventory_list)

@app.route('/resources', methods=['GET'])
def resources_route():
    resources = player.resources.get_all_resources()
    resources_list = [{'id': resource.id, 'name': resource.name, 'quantity': resource.quantity} for resource in resources]
    return jsonify(resources=resources_list)

@app.route('/collect_resources/<resource_id>/<quantity>', methods=['POST'])
def collect_resources_route(resource_id, quantity):
    result = player.resources.update_resource_quantity(resource_id, int(quantity))
    if result:
        return jsonify(result=result), 200
    else:
        return jsonify(error='Failed to update resource quantity'), 400

@app.route('/collect_resources/<resource_id>/<quantity>/<room_id>/<state_change>', methods=['POST'])
def collect_resources_state_change_route(resource_id, quantity, room_id, state_change):
    result = player.resources.update_resource_quantity(resource_id, int(quantity))
    current_room = game.map.get_room_by_id(room_id)
    current_room.room_resource_state_change(state_change, 'true')
    if result:
        return jsonify(result=result), 200
    else:
        return jsonify(error='Failed to update resource quantity'), 400
    
@app.route('/dialogues/start_npc/<room_id>/<npc_id>', methods=['GET'])
def dialogues_start_npc(room_id, npc_id):
    npc = game.map.get_room_by_id(room_id).get_npcs_by_id(npc_id) 
    try:
        dialogue_id, dialogue = game.dialogue_manager.start_dialogue(npc.dialogue_id)
        return jsonify({'dialogue_id': dialogue_id, 'dialogue': dialogue})
    except ValueError as e:
        print(e)
        return jsonify({'error': str(e)}), 400

@app.route('/dialogues/next/<dialogue_id>/<next_node>', methods=['GET'])
def next_node(dialogue_id, next_node):
    try:
        dialogue_id, result, actions = game.dialogue_manager.proceed_dialogue(dialogue_id, next_node)
        if actions:
            for action, arg in actions.items():
                action_registry.execute_action(action, game, player, context=arg) 

        if 'end' in result:
            # Dialogue has ended
            return jsonify(result), 200
        
        else:
            # Dialogue is continuing
            return jsonify({'dialogue_id': dialogue_id, 'dialogue': result}), 200
    except ValueError as e:
        print(e)
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)