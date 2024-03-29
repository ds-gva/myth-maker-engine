function createResourceHtml(tag, components) {
    var resourceId = components[1];
    var quantity = components[2];
    var text = components[3];
    var stateChange = components[4];
    return `<span class="resource-item underline underline-offset-4 text-amber-700 font-bold cursor-pointer" data-resource-id="${resourceId}" data-quantity="${quantity}" data-state="${stateChange}">${quantity} ${text}</span>`;
}

function pickUpResources(resourceId, quantity, roomId, stateChange) {
    fetch('/collect_resources/' + resourceId + '/' + quantity + '/' + roomId + '/' + stateChange, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            fetchAndUpdateResources()
            alert(data.result.message);
            getRoomDescription(roomId);
        });
}

function fetchAndUpdateResources() {
    fetch('/resources')
    .then(response => response.json())
    .then(data => {
        var resources = data.resources;
        var resourcesInventory = document.getElementById('resources-inventory');
        resourcesInventory.innerHTML = ''; // Clear the inventory

        resources.forEach(resource => {
            var resourceBox = document.createElement('div');
            resourceBox.className = 'resource-box p-4 border border-gray-300 rounded';

            var resourceName = document.createElement('h2');
            resourceName.className = 'text-xl font-bold';
            resourceName.textContent = resource.name;
            resourceBox.appendChild(resourceName);

            var resourceQuantity = document.createElement('p');
            resourceQuantity.textContent = 'Quantity: ' + resource.quantity;
            resourceBox.appendChild(resourceQuantity);

            resourcesInventory.appendChild(resourceBox);
        });
    });
}