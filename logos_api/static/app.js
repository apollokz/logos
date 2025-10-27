// logos_api/static/app.js

// --- 1. Определение наших пользовательских блоков ---

Blockly.defineBlocksWithJsonArray([
    // Блок для переменной (выпадающий список)
    {
        "type": "rule_variable",
        "message0": "%1",
        "args0": [
            {
                "type": "field_dropdown",
                "name": "VAR",
                "options": [
                    ["amount", "amount"],
                    ["risk_score", "risk_score"],
                    ["transaction_hour", "transaction_hour"]
                ]
            }
        ],
        "output": "String", // Этот блок можно будет вставить в другой блок
        "colour": 230,
        "tooltip": "Переменная для проверки"
    },
    // Блок для оператора (выпадающий список)
    {
        "type": "rule_operator",
        "message0": "%1",
        "args0": [
            {
                "type": "field_dropdown",
                "name": "OP",
                "options": [
                    ["<", "<"],
                    [">", ">"],
                    ["==", "=="],
                    ["<=", "<="],
                    [">=", ">="]
                ]
            }
        ],
        "output": "String",
        "colour": 160,
        "tooltip": "Оператор сравнения"
    },
    // Блок для значения (число)
    {
        "type": "rule_value",
        "message0": "%1",
        "args0": [
            {
                "type": "field_number",
                "name": "VALUE",
                "value": 0
            }
        ],
        "output": "Number",
        "colour": 290,
        "tooltip": "Значение для сравнения"
    },
    // Главный блок "Правило"
    {
        "type": "rule_statement",
        "message0": "Правило: %1 %2 %3",
        "args0": [
            { "type": "input_value", "name": "VAR", "check": "String" },
            { "type": "input_value", "name": "OP", "check": "String" },
            { "type": "input_value", "name": "VALUE", "check": "Number" }
        ],
        "previousStatement": null, // Можно соединять с блоком сверху
        "nextStatement": null,   // Можно соединять с блоком снизу
        "colour": 330,
        "tooltip": "Одно полное правило"
    }
]);

// --- 2. Конфигурация Панели Инструментов (Toolbox) ---

const toolbox = {
    "kind": "flyoutToolbox",
    "contents": [
        {
            "kind": "block",
            "type": "rule_statement"
        },
        {
            "kind": "block",
            "type": "rule_variable"
        },
        {
            "kind": "block",
            "type": "rule_operator"
        },
        {
            "kind": "block",
            "type": "rule_value"
        }
    ]
};

// --- 3. Инициализация рабочей области ---

const workspace = Blockly.inject('editor-container', {
    toolbox: toolbox // Используем нашу новую панель инструментов
});

console.log("Blockly workspace initialized with custom blocks.");
