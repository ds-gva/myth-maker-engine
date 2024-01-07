class ItemActions:
    _instance = None
    actions = {
        'pick_up': lambda game, character, item: ItemActions.pick_up(game, character, item),
        'drop': lambda game, character, item: ItemActions.drop(game, character, item),
    }

    @staticmethod
    def register_action(action_name, action_func):
        ItemActions.actions[action_name] = action_func

    @staticmethod
    def perform_action(action_name, game, character, item):
        action_func = ItemActions.actions.get(action_name)
        if action_func is not None:
            return action_func(game, character, item)
        else:
            raise ValueError(f"Action {action_name} is not defined.")

    @staticmethod
    def pick_up(game, character, item):
        if character.add_to_inventory(item):
            item.owner = character
            room = game.map.get_room_by_id(character.location)
            if item.dropped:
                del room.dropped_items[item.item_id]
                item.dropped = False
            else:
                del room.interactive_items[item.item_id]
            return {"success": True, "message": f"You picked up the {item.name}."}
        else:
            return {"success": False, "message": "You can't carry any more items."}

    @staticmethod
    def drop(game, character, item):
        if item.droppable == False:
            return {"success": False, "message": "You can't drop that item."}
        else:
            character.remove_from_inventory(item)
            room = game.map.get_room_by_id(character.location)
            item.owner = room
            item.dropped = True
            room.dropped_items[item.item_id] = item
            return {"success": True, "message": f"You dropped the {item.name}."}