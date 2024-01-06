function updateInventory(items, capacity) {
    console.log("Updating inventory with items:", items); 
    var inventoryItemsElement = document.getElementById('inventory-items');
    inventoryItemsElement.innerHTML = '';
    for (let i = 0; i < capacity; i++) {
        var li = document.createElement('li');
        li.classList.add('flex', 'items-center', 'justify-center', 'font-bold');
        if (items[i]) {
            li.textContent = items[i].name;
            li.classList.add('filled', 'bg-blue-600', 'hover:bg-blue-500', 'text-white', 'p-3', 'rounded-lg', 'transition', 'duration-200', 'ease-in-out', 'shadow-md', 'cursor-pointer');
            li.addEventListener('click', () => showModal(items[i].name, items[i].item_id));
        } else {
            li.textContent = 'empty';
            li.classList.add('empty', 'bg-gray-700', 'hover:bg-gray-600', 'text-gray-300', 'p-3', 'rounded-lg', 'transition', 'duration-200', 'ease-in-out', 'cursor-not-allowed');
        }
        inventoryItemsElement.appendChild(li);
    }
}

function fetchAndUpdateInventory() {
    fetch('/inventory')
        .then(response => response.json())
        .then(data => {
            updateInventory(data.inventory, data.inventory_capacity);
        });
}

document.addEventListener('DOMContentLoaded', (event) => {
    fetchAndUpdateInventory();
    document.getElementById('drop-button').addEventListener('click', function() {
        const itemId = document.getElementById('item-options-modal').dataset.id;
        console.log('Dropping item with id:', itemId)
        interactWithItem(itemId, 'drop');
        fetchAndUpdateInventory();
        closeModal();
    });
});

