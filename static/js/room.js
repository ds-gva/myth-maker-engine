function getRoomDescription(roomName) {
    fetch('/get_room_description/' + roomName, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            var description = data.description;
            var interactiveItemsData = data.interactive_items;
            for (var itemId in interactiveItemsData) {
                var itemData = interactiveItemsData[itemId];
                var itemHtml = `<span class="interactive-item inline-block px-2 py-1 m-1 bg-blue-500 text-white rounded-full cursor-pointer" data-item-id="${itemId}">${itemData.name}</span>`;
                var itemTag = "[" + itemId   + "]"; 
                console.log(itemTag)
                description = description.replace(itemTag, itemHtml);
                }

            document.getElementById('room-description').innerHTML = description; // Inject the description into the <p> element

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