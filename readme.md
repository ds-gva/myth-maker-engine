# Myth Maker Engine

Myth Maker Engine is a lightweight, text-based adventure game engine built with Python and Flask. It allows you to create your own interactive stories and adventures.

## Design Choices

- **Python**: We chose Python for its simplicity and readability. Python's extensive standard library and wide range of third-party packages also make it a great choice for a variety of projects.

- **Flask**: Flask is a lightweight and flexible web framework for Python. We chose Flask for its simplicity and ease of use, as well as its ability to scale up to complex applications.

- **Tailwind CSS**: Tailwind CSS is a utility-first CSS framework that is highly customizable and promotes component reuse. We chose Tailwind CSS for its flexibility and its ability to create responsive designs with ease.

- **Lightweight Design**: We aimed to keep the engine as lightweight and simple as possible. This makes it easy to understand, modify, and extend.

## Features

- Room-based navigation: Create a map of interconnected rooms for the player to explore.
- History tracking: Keep track of the player's journey through the game.
- Save and load game state: Players can save their progress and continue playing later.

## Installation

1. Clone this repository: `git clone https://github.com/yourusername/myth-maker-engine.git`
2. Navigate to the project directory: `cd myth-maker-engine`
3. Install the required packages: `pip install -r requirements.txt`
4. Run the application: `python app.py`

## Usage

To create a game, you need to define the game state and game map in JSON format. The game state includes the player's current location and history, and the game map defines the rooms and how they're connected.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the terms of the MIT license.

## Next Steps

* Implementing a dialogue system for NPCs
* Adding Player profile & characteristics (equipment & skill level)
* Creating a combat system
* Breaking down the game into chapters
* Improving the frontend