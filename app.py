from flask import Flask, request, render_template, redirect, url_for, jsonify
from game import Game, Player

app = Flask(__name__)
game = Game('game_data/initial_state.json', 'game_data/game_map.json')
player = game.get_character('PlayerName')

@app.route('/', methods=['GET', 'POST'])
def game_route():
    description = None
    interactive_items = None

    current_location = player.location
    print(current_location)
    current_room = game.map.get_room_by_id(current_location)

    if request.method == 'POST':
        direction = request.form.get('direction')
        target_room_id = current_room.directions[direction]['direction_id']
        if game.movement.can_move(player.location, direction, target_room_id):
            game.move_character(player.name, direction, target_room_id)
            current_room = game.map.get_room_by_id(target_room_id)
            print(f'Player moved {direction} to {target_room_id}')
        else:
            print("You can't go that way.")

    
    description = current_room.get_parsed_description()
    directions = current_room.directions

    return render_template('game.html',
                            room_name=current_room.name,
                            room_id=current_room.id,
                            description=description,
                            directions=directions,
                            history=player.history,
                            interactive_items=interactive_items)

@app.route('/get_room_description/<room_id>', methods=['POST'])
def get_room_description_route(room_id):
    current_room = game.map.get_room_by_id(room_id)
    description, interactive_items_data, npcs_data, dropped_items_data = current_room.get_parsed_description()

    return jsonify(description=description, interactive_items=interactive_items_data, npcs=npcs_data, dropped_items=dropped_items_data)

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
    inventory_capacity, inventory = player.get_inventory(as_dict=True)
    inventory_list = [{'name': item['name'], 'item_id': item['item_id']} for item in inventory]
    return jsonify(inventory_capacity=inventory_capacity, inventory=inventory_list)

if __name__ == '__main__':
    app.run(debug=True)