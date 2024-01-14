function getRoomDescription(roomId) {
    fetch('/get_room_description/' + roomId, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            var description = data.description;
            var interactiveItemsData = data.interactive_items;
            var npcsData = data.npcs;
            var droppedItems = data.dropped_items;

            for (var itemId in interactiveItemsData) {
                var itemHtml = createInteractiveItemHtml(itemId, interactiveItemsData[itemId]);
                description = description.replace("[" + itemId + "]", itemHtml);
            }

            for (var npcId in npcsData) {
                var npcHtml = createNpcHtml(npcId, npcsData[npcId]);
                description = description.replace("[" + npcId + "]", npcHtml);
            }

            var resourceTags = description.match(/\[resource: .+?]/g) || [];
            for (var i = 0; i < resourceTags.length; i++) {
                var tag = resourceTags[i];
                var components = tag.match(/resource: (.+?) \| (\d+) \| (.+?) \| (.+?)]/);
                var resourceHtml = createResourceHtml(tag, components);
                description = description.replace(tag, resourceHtml);
            }

            var droppedItemsHtml = '';
            for (var droppedItemId in droppedItems) {
                var droppedItemData = droppedItems[droppedItemId];
                if (droppedItemData) {
                    droppedItemsHtml += createDroppedItemHtml(droppedItemId, droppedItemData);
                }
            }

            document.getElementById('dropped-items').innerHTML = droppedItemsHtml ? "On the floor, you dropped: " + droppedItemsHtml : '';
            document.getElementById('room-description').innerHTML = description;

            document.querySelectorAll('.interactive-item').forEach(item => {
                item.addEventListener('click', () => inspectItem(item.dataset.itemId));
            });

            document.querySelectorAll('.resource-item').forEach(resource => {
                resource.addEventListener('click', () => pickUpResources(resource.dataset.resourceId, resource.dataset.quantity, roomId, resource.dataset.state));
            });

               document.querySelectorAll('[data-npc-id]').forEach(npcElement => {
                npcElement.addEventListener('click', function() {
                    var npcId = npcElement.getAttribute('data-npc-id');
                    fetch('/dialogues/start_npc/' + roomId + '/' + npcId)
                        .then(response => response.json())
                        .then(data => {
                            displayDialogue(data.dialogue_id, data.dialogue, npcId);
                        });
            });
    });
        });

        
}

window.onload = function() {
    var roomId = document.querySelector('div[data-room-id]').dataset.roomId;
    getRoomDescription(roomId);
    fetchAndUpdateResources();
    fetchAndUpdateInventory();
}