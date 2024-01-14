function createNpcHtml(npcId, npcData) {
    var npcElement = document.createElement('span');
    npcElement.className = 'npc cursor-pointer text-blue-600 border-b-2 border-dotted border-blue-600 font-bold';
    npcElement.dataset.npcId = npcId;
    npcElement.textContent = npcData.name;

    return npcElement.outerHTML;
}
