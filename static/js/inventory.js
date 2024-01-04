function updateInventory(items) {
    console.log("Updating inventory with items:", items); 
    var inventoryItemsElement = document.getElementById('inventory-items');
    inventoryItemsElement.innerHTML = '';
    items.forEach(function(item) {
        var li = document.createElement('li');
        li.textContent = item.name;
        inventoryItemsElement.appendChild(li);
    });
}

function fetchAndUpdateInventory() {
    fetch('/inventory')
        .then(response => response.json())
        .then(data => {
            console.log("Received data from /inventory:", data);
            updateInventory(data.inventory);
        });
}

document.addEventListener('DOMContentLoaded', (event) => {
    fetchAndUpdateInventory();
});