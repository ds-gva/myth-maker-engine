function pickUpResrouces(resourceId, quantity, roomId, stateChange) {
    fetch('/collect_resources/' + resourceId + '/' + quantity + '/' + roomId + '/' + stateChange, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            getRoomDescription(roomId);
            fetchAndUpdateResources()
            alert(data.result.message);
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