// logos_api/static/app.js

// ... (весь предыдущий код Blockly и Дашборда остается без изменений) ...
Blockly.defineBlocksWithJsonArray([ { "type": "rule_variable", "message0": "%1", "args0": [ { "type": "field_dropdown", "name": "VAR", "options": [ ["amount", "amount"], ["risk_score", "risk_score"], ["transaction_hour", "transaction_hour"] ] } ], "output": "String", "colour": 230, "tooltip": "Переменная для проверки" }, { "type": "rule_operator", "message0": "%1", "args0": [ { "type": "field_dropdown", "name": "OP", "options": [ ["<", "<"], [">", ">"], ["==", "=="], ["<=", "<="], [">=", ">="] ] } ], "output": "String", "colour": 160, "tooltip": "Оператор сравнения" }, { "type": "rule_value", "message0": "%1", "args0": [ { "type": "field_number", "name": "VALUE", "value": 0 } ], "output": "Number", "colour": 290, "tooltip": "Значение для сравнения" }, { "type": "rule_statement", "message0": "Правило: %1 %2 %3", "args0": [ { "type": "input_value", "name": "VAR", "check": "String" }, { "type": "input_value", "name": "OP", "check": "String" }, { "type": "input_value", "name": "VALUE", "check": "Number" } ], "previousStatement": null, "nextStatement": null, "colour": 330, "tooltip": "Одно полное правило" } ]);
const toolbox = { "kind": "flyoutToolbox", "contents": [ { "kind": "block", "type": "rule_statement" }, { "kind": "block", "type": "rule_variable" }, { "kind": "block", "type": "rule_operator" }, { "kind": "block", "type": "rule_value" } ] };
const workspace = Blockly.inject('editor-container', { toolbox: toolbox });
const ruleGenerator = new Blockly.Generator('JSON');
ruleGenerator.forBlock['rule_statement'] = function(block, generator) { const variable = generator.valueToCode(block, 'VAR', 0) || 'null'; const operator = generator.valueToCode(block, 'OP', 0) || 'null'; const value = generator.valueToCode(block, 'VALUE', 0) || 'null'; return `${variable.replace(/'/g, '')} ${operator.replace(/'/g, '')} ${value}`; };
ruleGenerator.forBlock['rule_variable'] = function(block, generator) { return [block.getFieldValue('VAR'), 0]; };
ruleGenerator.forBlock['rule_operator'] = function(block, generator) { return [block.getFieldValue('OP'), 0]; };
ruleGenerator.forBlock['rule_value'] = function(block, generator) { return [block.getFieldValue('VALUE'), 0]; };
const saveButton = document.getElementById('save-button');
const outputArea = document.getElementById('output');
saveButton.addEventListener('click', () => { const topBlocks = workspace.getTopBlocks(true); const rules = topBlocks.map(block => ruleGenerator.blockToCode(block)); const ruleset = { description: "Набор правил, сгенерированный редактором", rules: rules }; outputArea.textContent = JSON.stringify(ruleset, null, 2); });
console.log("Blockly workspace and code generator initialized.");
const refreshButton = document.getElementById('refresh-history-button');
const historyTableBody = document.getElementById('history-table-body');
const apiKey = "LOGOS_SECRET_MVP2_KEY";
async function fetchAndDisplayHistory() { try { const response = await fetch('/api/history', { headers: { 'accept': 'application/json', 'X-API-Key': apiKey } }); if (!response.ok) { throw new Error(`HTTP error! status: ${response.status}`); } const history = await response.json(); historyTableBody.innerHTML = ''; history.forEach(entry => { const row = historyTableBody.insertRow(); const cell1 = row.insertCell(0); const cell2 = row.insertCell(1); const cell3 = row.insertCell(2); cell1.textContent = entry.timestamp; cell2.textContent = entry.request_prompt; cell3.textContent = entry.response_result; }); } catch (error) { console.error("Could not fetch history:", error); historyTableBody.innerHTML = '<tr><td colspan="3">Ошибка при загрузке истории.</td></tr>'; } }
refreshButton.addEventListener('click', fetchAndDisplayHistory);
document.addEventListener('DOMContentLoaded', fetchAndDisplayHistory);
console.log("History dashboard initialized.");

// --- ИЗМЕНЕНИЕ: 6. Логика Stripe Checkout ---

// ВАЖНО: Используйте ваш тестовый ПУБЛИЧНЫЙ ключ (pk_test_...)
const stripe = Stripe("pk_live_51P28lOADBlo4U7jNI2LkWd3bBlcm3ELC6GqDlUAHSfOII2xxFVwGkYqDWpBXfJM63Spdcqg85rgzYGROhtQDKtIk00Fz6kC5pP"); // ЗАМЕНИТЕ ЭТО НА СВОЙ ПУБЛИЧНЫЙ ТЕСТОВЫЙ КЛЮЧ
const checkoutButton = document.getElementById('checkout-button');

checkoutButton.addEventListener('click', async function () {
    try {
        // 1. Запрашиваем ID сессии у нашего бэкенда
        const response = await fetch('/api/create-checkout-session', {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'X-API-Key': apiKey
            }
        });

        const session = await response.json();

        if (session.session_id) {
            // 2. Если сессия создана, перенаправляем пользователя на страницу оплаты Stripe
            const result = await stripe.redirectToCheckout({
                sessionId: session.session_id
            });
            if (result.error) {
                // Если возникла ошибка на стороне клиента, показываем ее
                alert(result.error.message);
            }
        } else {
             alert("Не удалось создать платежную сессию.");
        }
    } catch (error) {
        console.error("Stripe checkout error:", error);
        alert("Произошла ошибка при переходе к оплате.");
    }
});

console.log("Stripe checkout initialized.");
