
function inspectItem(itemId) {
    var itemDescriptionElement = document.getElementById('item-description');
    var itemTitleElement = document.getElementById('item-title');
    var itemTextElement = document.getElementById('item-text');
    var itemActionsElement = document.getElementById('item-actions');

    fetch('/inspect_item/' + itemId, { method: 'POST' })  // Use the item ID in the fetch request
        .then(response => response.json())
        .then(data => {
            itemTitleElement.textContent = data.item_name;
            itemTextElement.textContent = data.item_description;
            itemActionsElement.innerHTML = '';
            data.item_actions.forEach(function(action) {
                var button = document.createElement('button');
                button.textContent = action;
                button.classList.add('action-button', 'px-2', 'py-1', 'm-1', 'bg-green-500', 'text-white', 'rounded-full');
                button.addEventListener('click', function() {
                    interactWithItem(itemId, action);
                });
                itemActionsElement.appendChild(button);
            });
            itemDescriptionElement.classList.remove('hidden');
        });
}

function clearInspectItem() {
    var itemDescriptionElement = document.getElementById('item-description');
    itemDescriptionElement.classList.add('hidden');
}

function interactWithItem(itemId, action) {
    fetch('/interact_with_item/' + itemId + '/' + action, { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        var roomName = document.querySelector('div[data-room-name]').dataset.roomName;
        fetchAndUpdateInventory();
        getRoomDescription(roomName);
        clearInspectItem();
    });
}