# Myth Maker Engine

Myth Maker Engine is a lightweight, text-based adventure game engine built with Python. It allows you to create your own interactive stories and adventures.
Backend is pure Python and is headless. Frontend can then easily be built either using a Flask application or even a command line.

## Engine Structure

The game engine is organized into several modules, each responsible for a different aspect of the game:

- **Characters**: This module contains the `Character`, `Player`, `NPC`, and `Inventory` classes. These classes represent the characters in the game and their inventories.

- **Items**: This module contains the `Item` and `ItemsManager` classes. These classes represent the items that can be found in the game and manage the interactions between characters and items.

- **Rooms**: This module contains the `Room` class, which represents a room in the game.

- **Map**: This module contains the `Map` and `MapLoader` classes. These classes manage the game map and handle loading the map from a JSON file.

- **Movement**: This module contains the `Movement` class, which handles character movement.

- **Game**: This module contains the `Game` class, which is the main class for the game logic. It manages the game state and handles interactions between the other classes.

## License

This project is licensed under the terms of the MIT license.

## Next Steps

* Implementing a dialogue system for NPCs
* Adding Player profile & characteristics (equipment & skill level)
* Creating a combat system
* Breaking down the game into chapters
* Improving the frontend