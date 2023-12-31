from flask import Flask, request, render_template, redirect, url_for
from game import Game

app = Flask(__name__)
game = Game('game_data/initial_state.json', 'game_data/game_map.json')

@app.route('/', methods=['GET', 'POST'])
def game_route():
    if request.method == 'POST':
        direction = request.form.get('direction')
        game.move(direction)
    current_location = game.state['location']
    description = game.map[current_location].description
    directions = game.map[current_location].directions
    return render_template('game.html', location=current_location, description=description, directions=directions, history=game.state['history'])

@app.route('/save', methods=['POST'])
def save():
    game.save_state()
    return redirect(url_for('game_route'))

@app.route('/load', methods=['POST'])
def load():
    game.load_state()
    return redirect(url_for('game_route'))

if __name__ == '__main__':
    app.run(debug=True)