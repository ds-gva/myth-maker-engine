function createInteractiveItemHtml(itemId, itemData) {
    return `<span class="interactive-item inline-block px-2 bg-blue-500 text-white font-bold rounded-full cursor-pointer" data-item-id="${itemId}">${itemData.name}</span>`;
}

function createNpcHtml(npcId, npcData) {
    return `<span class="npc cursor-pointer text-blue-600 border-b-2 border-dotted border-blue-600 font-bold" data-npc-id="${npcId}">${npcData.name}</span>`;
}

function createResourceHtml(tag, components) {
    var resourceId = components[1];
    var quantity = components[2];
    var text = components[3];
    var stateChange = components[4];
    return `<span class="resource-item underline underline-offset-4 text-amber-700 font-bold cursor-pointer" data-resource-id="${resourceId}" data-quantity="${quantity}" data-state="${stateChange}">${quantity} ${text}</span>`;
}

function createDroppedItemHtml(droppedItemId, droppedItemData) {
    return `<span class="interactive-item inline-block px-2 bg-blue-500 text-white font-bold rounded-full cursor-pointer" data-item-id="${droppedItemId}">${droppedItemData.name}</span>`;
}

function getRoomDescription(roomId) {
    console.log(roomId)
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
                resource.addEventListener('click', () => pickUpResrouces(resource.dataset.resourceId, resource.dataset.quantity, roomId, resource.dataset.state));
            });
        });
}

window.onload = function() {
    var roomId = document.querySelector('div[data-room-id]').dataset.roomId;
    getRoomDescription(roomId);
}