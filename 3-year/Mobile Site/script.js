class RootCalculator {
    constructor() {
        this.history = JSON.parse(localStorage.getItem('calculationHistory')) || [];
        this.settings = JSON.parse(localStorage.getItem('appSettings')) || {
            decimalPlaces: 4,
            saveHistory: true
        };
        
        this.initializeElements();
        this.loadSettings();
        this.attachEventListeners();
    }

    initializeElements() {
        // Основные элементы
        this.numberInput = document.getElementById('numberInput');
        this.calculateBtn = document.getElementById('calculateBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.resultDiv = document.getElementById('result');
        
        // Радио-кнопки
        this.squareRootRadio = document.getElementById('squareRoot');
        this.cubeRootRadio = document.getElementById('cubeRoot');
        
        // Навигация
        this.historyBtn = document.getElementById('historyBtn');
        this.settingsBtn = document.getElementById('settingsBtn');
        this.backFromHistory = document.getElementById('backFromHistory');
        this.backFromSettings = document.getElementById('backFromSettings');
        
        // Экраны
        this.mainScreen = document.getElementById('mainScreen');
        this.historyScreen = document.getElementById('historyScreen');
        this.settingsScreen = document.getElementById('settingsScreen');
        
        // История
        this.historyList = document.getElementById('historyList');
        this.clearHistoryBtn = document.getElementById('clearHistory');
        
        // Настройки
        this.decimalPlacesSelect = document.getElementById('decimalPlaces');
        this.saveHistoryCheckbox = document.getElementById('saveHistory');
    }

    attachEventListeners() {
        // Кнопки вычисления
        this.calculateBtn.addEventListener('click', () => this.calculate());
        this.clearBtn.addEventListener('click', () => this.clear());
        
        // Навигация
        this.historyBtn.addEventListener('click', () => this.showScreen('history'));
        this.settingsBtn.addEventListener('click', () => this.showScreen('settings'));
        this.backFromHistory.addEventListener('click', () => this.showScreen('main'));
        this.backFromSettings.addEventListener('click', () => this.showScreen('main'));
        
        // История
        this.clearHistoryBtn.addEventListener('click', () => this.clearHistory());
        
        // Настройки
        this.decimalPlacesSelect.addEventListener('change', () => this.saveSettings());
        this.saveHistoryCheckbox.addEventListener('change', () => this.saveSettings());
        
        // Ввод по Enter
        this.numberInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.calculate();
            }
        });
    }

    calculate() {
        const number = parseFloat(this.numberInput.value);
        const rootType = document.querySelector('input[name="rootType"]:checked').value;
        
        // Проверка на пустой ввод
        if (isNaN(number)) {
            this.showResult('Ошибка: Введите число', true);
            return;
        }
        
        // Проверка на отрицательные числа для квадратного корня
        if (rootType === 'square' && number < 0) {
            this.showResult('Ошибка: Нельзя извлекать квадратный корень из отрицательного числа', true);
            return;
        }
        
        let result;
        if (rootType === 'square') {
            result = Math.sqrt(number);
        } else {
            result = Math.cbrt(number);
        }
        
        const formattedResult = result.toFixed(this.settings.decimalPlaces);
        const symbol = rootType === 'square' ? '√' : '∛';
        
        this.showResult(`${symbol}${number} = ${formattedResult}`);
        
        // Сохранение в историю
        if (this.settings.saveHistory) {
            this.addToHistory(number, rootType, result);
        }
    }

    showResult(message, isError = false) {
        this.resultDiv.textContent = message;
        this.resultDiv.style.background = isError ? '#ffe6e6' : '#f0f9ff';
        this.resultDiv.style.borderColor = isError ? '#ff4444' : '#4facfe';
        this.resultDiv.style.color = isError ? '#cc0000' : '#333';
    }

    clear() {
        this.numberInput.value = '';
        this.resultDiv.textContent = '';
        this.resultDiv.style.background = '#f8f9fa';
        this.resultDiv.style.borderColor = '#e1e5e9';
        this.numberInput.focus();
    }

    addToHistory(number, type, result) {
        const historyItem = {
            id: Date.now(),
            number: number,
            type: type,
            result: result,
            timestamp: new Date().toLocaleString('ru-RU'),
            decimalPlaces: this.settings.decimalPlaces
        };
        
        this.history.unshift(historyItem);
        
        // Ограничиваем историю 50 записями
        if (this.history.length > 50) {
            this.history.pop();
        }
        
        this.saveHistory();
        this.updateHistoryDisplay();
    }

    updateHistoryDisplay() {
        this.historyList.innerHTML = '';
        
        if (this.history.length === 0) {
            this.historyList.innerHTML = '<div class="history-item">История вычислений пуста</div>';
            return;
        }
        
        this.history.forEach(item => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            const symbol = item.type === 'square' ? '√' : '∛';
            historyItem.textContent = `${symbol}${item.number} = ${item.result.toFixed(item.decimalPlaces)} (${item.timestamp})`;
            this.historyList.appendChild(historyItem);
        });
    }

    clearHistory() {
        if (confirm('Вы уверены, что хотите очистить историю вычислений?')) {
            this.history = [];
            this.saveHistory();
            this.updateHistoryDisplay();
        }
    }

    showScreen(screenName) {
        // Скрываем все экраны
        this.mainScreen.classList.remove('active');
        this.historyScreen.classList.remove('active');
        this.settingsScreen.classList.remove('active');
        
        // Показываем нужный экран
        switch(screenName) {
            case 'main':
                this.mainScreen.classList.add('active');
                break;
            case 'history':
                this.historyScreen.classList.add('active');
                this.updateHistoryDisplay();
                break;
            case 'settings':
                this.settingsScreen.classList.add('active');
                break;
        }
    }

    loadSettings() {
        this.decimalPlacesSelect.value = this.settings.decimalPlaces;
        this.saveHistoryCheckbox.checked = this.settings.saveHistory;
    }

    saveSettings() {
        this.settings = {
            decimalPlaces: parseInt(this.decimalPlacesSelect.value),
            saveHistory: this.saveHistoryCheckbox.checked
        };
        
        localStorage.setItem('appSettings', JSON.stringify(this.settings));
    }

    saveHistory() {
        localStorage.setItem('calculationHistory', JSON.stringify(this.history));
    }
}

// Инициализация приложения когда DOM загружен
document.addEventListener('DOMContentLoaded', () => {
    new RootCalculator();
});

// Добавляем поддержку PWA
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker зарегистрирован');
            })
            .catch(function(error) {
                console.log('Ошибка регистрации ServiceWorker:', error);
            });
    });
}