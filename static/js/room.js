function getRoomDescription(roomName) {
    fetch('/get_room_description/' + roomName, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            var description = data.description;
            var interactiveItemsData = data.interactive_items;
            var npcsData = data.npcs;
            var droppedItems = data.dropped_items;

            for (var itemId in interactiveItemsData) {
                var itemData = interactiveItemsData[itemId];
                var itemHtml = `<span class="interactive-item inline-block px-2 bg-blue-500 text-white font-bold rounded-full cursor-pointer" data-item-id="${itemId}">${itemData.name}</span>`;
                var itemTag = "[" + itemId   + "]"; 
                console.log(itemTag)
                description = description.replace(itemTag, itemHtml);
                }

            for (var npcId in npcsData) {
                var npcData = npcsData[npcId];
                var npcHtml = `<span class="npc cursor-pointer text-blue-600 border-b-2 border-dotted border-blue-600 font-bold" data-npc-id="${npcId}">${npcData.name}</span>`;
                var npcTag = "[" + npcId + "]"; 
                description = description.replace(npcTag, npcHtml);
            }

            var droppedItemsElement = document.getElementById('dropped-items');
            var droppedItemsHtml = '';
            
            for (var droppedItemId in droppedItems) {
                var droppedItemData = droppedItems[droppedItemId];
                if (droppedItemData) {
                    droppedItemsHtml += `<span class="interactive-item inline-block px-2 bg-blue-500 text-white font-bold rounded-full cursor-pointer" data-item-id="${droppedItemId}">${droppedItemData.name}</span>`;
                }
            }
            
            if (droppedItemsHtml) {
                droppedItemsElement.innerHTML = "On the floor, you dropped: " + droppedItemsHtml;
            } else {    
                droppedItemsElement.textContent = '';
            }
            
            document.getElementById('room-description').innerHTML = description; // 

            var interactiveItems = document.querySelectorAll('.interactive-item');
            interactiveItems.forEach(function(item) {
                item.addEventListener('click', function() {
                var itemId = item.dataset.itemId;  // Get the item ID
                inspectItem(itemId);
            });
        });
    });
}


window.onload = function() {
    var roomName = document.querySelector('div[data-room-name]').dataset.roomName;
    getRoomDescription(roomName);
}