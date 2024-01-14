function createInteractiveItemHtml(itemId, itemData) {
    return `<span class="interactive-item inline-block px-2 bg-blue-500 text-white font-bold rounded-full cursor-pointer" data-item-id="${itemId}">${itemData.name}</span>`;
}

function createDroppedItemHtml(droppedItemId, droppedItemData) {
    return `<span class="interactive-item inline-block px-2 bg-blue-500 text-white font-bold rounded-full cursor-pointer" data-item-id="${droppedItemId}">${droppedItemData.name}</span>`;
}

function updateInventory(items, capacity) {
    var inventoryItemsElement = document.getElementById('inventory-items');
    inventoryItemsElement.innerHTML = '';
    for (let i = 0; i < capacity; i++) {
        var li = document.createElement('li');
        li.classList.add('flex', 'items-center', 'justify-center', 'font-bold');
        if (items[i]) {
            li.textContent = items[i].name + " (" + items[i].quantity + ")";
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
        interactWithItem(itemId, 'drop');
        fetchAndUpdateInventory();
        closeModal();
    });
});

