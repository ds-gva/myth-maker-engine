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


# Using Conditions in the Game

Conditions in the game are used to dynamically change the text and behavior based on the game state. They are defined in the `dynamic_text` field of the room descriptions in the JSON data.

## Structure of a Condition

A condition is defined as an object with two fields: `condition` and `text`. The `condition` field is the name of the game state variable that the condition checks, and the `text` field is the text that will be used if the condition is `true`.

Here's an example of a condition:

```json
{
    "condition": "trees_chopped",
    "text": "There is a pile of chopped wood in the corner of the garden."
}```

In this example, if the `trees_chopped` game state variable is `true`, then the text "There is a pile of chopped wood in the corner of the garden." will be used.

## Using Multiple Conditions
You can define multiple conditions for a single piece of dynamic text. The conditions are checked in the order they are defined, and the text for the last `true` condition will be used.

Here's an example of multiple conditions:

```json
"dynamic_text": {
    "tree1_description": {
        "default": "There is a patch of trees in the corner of the garden.",
        "conditions": [
            {
                "condition": "trees_chopped",
                "text": "There is a pile of chopped wood in the corner of the garden."
            },
            {
                "condition": "wood_taken",
                "text": "A few stubs of wood in the corner of the garden."
            }
        ]
    }
}
```
In this example, if `trees_chopped` is true but `wood_taken` is `false`, then the text for the `trees_chopped` condition will be used. If both `trees_chopped` and `wood_taken` are `true`, then the text for the `wood_taken` condition will be used, because it is the last `true` condition.

## Changing the Game State
The game state can be changed by the player's actions. For example, if the player chops down a tree, you might set the `trees_chopped` game state variable to `true`. This would then change the room description to use the text for the `trees_chopped` condition.

To change the game state, you can use the `room_resource_state_change` method of the `Room` class. This method takes two arguments: the name of the game state variable to change, and the new value for the variable. For example, to set `trees_chopped` to true, you would call `room_resource_state_change('trees_chopped', 'true')`.

Remember to carefully manage the game state to ensure that the conditions work as expected. If a condition being `true` means that another condition should be `false`, then you need to handle that in your game logic.

## License

This project is licensed under the terms of the MIT license.

## Next Steps

* Implementing a dialogue system for NPCs
* Adding Player profile & characteristics (equipment & skill level)
* Creating a combat system
* Breaking down the game into chapters
* Improving the frontend