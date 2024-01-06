document.addEventListener('DOMContentLoaded', (event) => {
    var tabButtons = document.querySelectorAll('.tab-button');
    var tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var tabId = button.dataset.tab;

            tabButtons.forEach(function(btn) {
                btn.classList.toggle('text-yellow-500', btn === button);
                btn.classList.toggle('border-yellow-500', btn === button);
                btn.classList.toggle('text-white', btn !== button);
                btn.classList.toggle('border-transparent', btn !== button);
            });

            tabContents.forEach(function(content) {
                content.classList.toggle('hidden', content.id !== tabId);
            });
        });
    });
    
});


function showModal(itemName, itemId) {
    document.getElementById('item-name').innerText = itemName;
    document.getElementById('item-options-modal').dataset.id = itemId;
    console.log(document.getElementById('item-options-modal'))   
    document.getElementById('item-options-modal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('item-options-modal').classList.add('hidden');
}