// logos_api/static/app.js

// Инициализируем рабочую область Blockly
// Мы "внедряем" редактор в наш div с id 'editor-container'
const workspace = Blockly.inject('editor-container', {
    // На данном этапе мы не добавляем никаких инструментов (блоков),
    // поэтому панель инструментов будет пустой.
    toolbox: {
        "kind": "flyoutToolbox",
        "contents": []
    }
});

console.log("Blockly workspace initialized.");
