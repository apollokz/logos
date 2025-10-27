// logos_api/static/app.js

// --- 1. Определение наших пользовательских блоков ---
Blockly.defineBlocksWithJsonArray([
    { "type": "rule_variable", "message0": "%1", "args0": [ { "type": "field_dropdown", "name": "VAR", "options": [ ["amount", "amount"], ["risk_score", "risk_score"], ["transaction_hour", "transaction_hour"] ] } ], "output": "String", "colour": 230, "tooltip": "Переменная для проверки" },
    { "type": "rule_operator", "message0": "%1", "args0": [ { "type": "field_dropdown", "name": "OP", "options": [ ["<", "<"], [">", ">"], ["==", "=="], ["<=", "<="], [">=", ">="] ] } ], "output": "String", "colour": 160, "tooltip": "Оператор сравнения" },
    { "type": "rule_value", "message0": "%1", "args0": [ { "type": "field_number", "name": "VALUE", "value": 0 } ], "output": "Number", "colour": 290, "tooltip": "Значение для сравнения" },
    { "type": "rule_statement", "message0": "Правило: %1 %2 %3", "args0": [ { "type": "input_value", "name": "VAR", "check": "String" }, { "type": "input_value", "name": "OP", "check": "String" }, { "type": "input_value", "name": "VALUE", "check": "Number" } ], "previousStatement": null, "nextStatement": null, "colour": 330, "tooltip": "Одно полное правило" }
]);

// --- 2. Конфигурация Панели Инструментов (Toolbox) ---
const toolbox = { "kind": "flyoutToolbox", "contents": [ { "kind": "block", "type": "rule_statement" }, { "kind": "block", "type": "rule_variable" }, { "kind": "block", "type": "rule_operator" }, { "kind": "block", "type": "rule_value" } ] };

// --- 3. Инициализация рабочей области ---
const workspace = Blockly.inject('editor-container', { toolbox: toolbox });

// --- ИЗМЕНЕНИЕ: 4. Генератор кода и обработчик кнопки ---

// Создаем новый "генератор кода"
const ruleGenerator = new Blockly.Generator('JSON');

// Описываем, как превращать наш главный блок в строку
ruleGenerator.forBlock['rule_statement'] = function(block, generator) {
    const variable = generator.valueToCode(block, 'VAR', 0) || 'null';
    const operator = generator.valueToCode(block, 'OP', 0) || 'null';
    const value = generator.valueToCode(block, 'VALUE', 0) || 'null';
    // Убираем кавычки, которые Blockly добавляет по умолчанию
    return `${variable.replace(/'/g, '')} ${operator.replace(/'/g, '')} ${value}`;
};
// Описываем, как превращать остальные блоки в их значения
ruleGenerator.forBlock['rule_variable'] = function(block, generator) { return [block.getFieldValue('VAR'), 0]; };
ruleGenerator.forBlock['rule_operator'] = function(block, generator) { return [block.getFieldValue('OP'), 0]; };
ruleGenerator.forBlock['rule_value'] = function(block, generator) { return [block.getFieldValue('VALUE'), 0]; };

// Находим кнопку и область вывода
const saveButton = document.getElementById('save-button');
const outputArea = document.getElementById('output');

// Добавляем обработчик нажатия на кнопку
saveButton.addEventListener('click', () => {
    // Получаем все блоки верхнего уровня
    const topBlocks = workspace.getTopBlocks(true);
    // Превращаем каждый блок в строку правила с помощью нашего генератора
    const rules = topBlocks.map(block => ruleGenerator.blockToCode(block));
    
    // Формируем финальный JSON-объект
    const ruleset = {
        description: "Набор правил, сгенерированный редактором",
        rules: rules
    };
    
    // Красиво выводим JSON в нашу область <pre>
    outputArea.textContent = JSON.stringify(ruleset, null, 2);
});

console.log("Blockly workspace and code generator initialized.");
