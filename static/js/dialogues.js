function displayDialogue(dialogueId, node, npcId) {
    var dialogueBox = document.getElementById('dialogueBox');
    dialogueBox.classList.remove('hidden');

    var npcNameElement = document.getElementById('npcName');
    npcNameElement.textContent = npcId;

    // Add dialogue text
    var dialogueTextElement = document.getElementById('dialogueText');
    dialogueTextElement.textContent = node.text;

    // Add player choices
    var choicesElement = document.getElementById('choices');
    choicesElement.innerHTML = ''; // clear previous choices

    node.choices.forEach(choice => {
        var choiceElement = document.createElement('button');
        choiceElement.className = 'mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm';
        choiceElement.textContent = choice.text;
        choiceElement.addEventListener('click', function() {
            if (choice.next_node === null) {
                // End of dialogue, hide dialogue box
                var dialogueBox = document.getElementById('dialogueBox');
                if (dialogueBox) {
                    dialogueBox.classList.add('hidden');
                }
            } else {
                fetch('/dialogues/next/' + dialogueId + '/' + choice.next_node)
                    .then(response => response.json())
                    .then(data => {
                        displayDialogue(data.dialogue_id, data.dialogue, npcId);
                    });
            }
        });
        choicesElement.appendChild(choiceElement);
    });

    // Replace old dialogue box with new one
    var oldDialogueBox = document.getElementById('dialogueBox');
    if (oldDialogueBox) {
        oldDialogueBox.parentNode.replaceChild(dialogueBox, oldDialogueBox);
    } else {
        document.body.appendChild(dialogueBox);
    }
}