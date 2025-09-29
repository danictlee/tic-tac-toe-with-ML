class TicTacToeGame {
    constructor() {
        this.gameState = null;
        this.gameHistory = [];
        this.stats = {
            gamesPlayed: 0,
            predictionsCorrect: 0,
            predictionsTotal: 0
        };
        this.initializeGame();
        this.bindEvents();
        this.loadGameHistory();
    }

    initializeGame() {
        this.fetchGameState();
    }

    bindEvents() {
        // Game board cell clicks
        document.querySelectorAll('.cell').forEach((cell, index) => {
            cell.addEventListener('click', () => this.makeMove(index));
        });

        // Control buttons
        document.getElementById('resetBtn').addEventListener('click', () => this.resetGame());
        document.getElementById('aiMoveBtn').addEventListener('click', () => this.makeAIMove());

        // Clear history button
        const clearHistoryBtn = document.getElementById('clearHistoryBtn');
        if (clearHistoryBtn) {
            clearHistoryBtn.addEventListener('click', () => this.clearHistory());
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'r' && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                this.resetGame();
            } else if (e.key === ' ' && this.gameState && !this.gameState.gameOver && this.gameState.currentPlayer === 'O') {
                e.preventDefault();
                this.makeAIMove();
            }
        });
    }

    async fetchGameState() {
        try {
            this.showLoading(true);
            const response = await fetch('/game_state');
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('Game state received:', data); // Debug log
            this.gameState = data;
            this.updateUI();
        } catch (error) {
            console.error('Error fetching game state:', error);
            this.showError(`Failed to fetch game state: ${error.message}`);
            
            // Initialize with default state if fetch fails
            this.gameState = {
                board: ['', '', '', '', '', '', '', '', ''],
                currentPlayer: 'X',
                gameOver: false,
                winner: null,
                prediction: null
            };
            this.updateUI();
        } finally {
            this.showLoading(false);
        }
    }

    async makeMove(position) {
        if (!this.gameState || this.gameState.gameOver || !this.gameState.board || this.gameState.board[position] !== '') {
            return;
        }

        try {
            this.showLoading(true);
            const response = await fetch('/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ position: position })
            });

            const data = await response.json();
            
            if (data.error) {
                this.showError(data.error);
                return;
            }

            this.gameState = data;
            this.updateUI();
            
            // Add to history if prediction was made
            if (data.prediction) {
                this.addToHistory(data);
            }

        } catch (error) {
            console.error('Error making move:', error);
            this.showError('Failed to make move');
        } finally {
            this.showLoading(false);
        }
    }

    async makeAIMove() {
        if (!this.gameState || this.gameState.gameOver || this.gameState.currentPlayer !== 'O') {
            return;
        }

        try {
            this.showLoading(true);
            const response = await fetch('/ai_move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();
            
            if (data.error) {
                this.showError(data.error);
                return;
            }

            this.gameState = data;
            this.updateUI();
            
            // Add to history if prediction was made
            if (data.prediction) {
                this.addToHistory(data);
            }

        } catch (error) {
            console.error('Error making AI move:', error);
            this.showError('Failed to make AI move');
        } finally {
            this.showLoading(false);
        }
    }

    async resetGame() {
        try {
            this.showLoading(true);
            const response = await fetch('/reset', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();
            this.gameState = data;
            this.updateUI();
            this.clearPredictionDisplay();
            
            // Increment games played counter
            this.stats.gamesPlayed++;
            this.updateStatsDisplay();

        } catch (error) {
            console.error('Error resetting game:', error);
            this.showError('Failed to reset game');
        } finally {
            this.showLoading(false);
        }
    }

    updateUI() {
        this.updateBoard();
        this.updateGameStatus();
        this.updateControls();
        this.updatePredictionDisplay();
        this.updateStatsDisplay();
    }

    updateBoard() {
        if (!this.gameState || !this.gameState.board) {
            console.warn('Game state or board not available for updateBoard');
            return;
        }
        
        const cells = document.querySelectorAll('.cell');
        cells.forEach((cell, index) => {
            const value = this.gameState.board[index] || '';
            cell.textContent = value;
            cell.className = 'cell';
            
            if (value !== '') {
                cell.classList.add(value.toLowerCase());
                cell.disabled = true;
            } else {
                cell.disabled = this.gameState.gameOver || this.gameState.currentPlayer === 'O';
            }
        });

        // Highlight winning combination if game is over
        if (this.gameState.gameOver && this.gameState.winner && this.gameState.winner !== 'Draw') {
            this.highlightWinningCombination();
        }
    }

    updateGameStatus() {
        if (!this.gameState) {
            console.warn('Game state not available for updateGameStatus');
            return;
        }
        
        const statusElement = document.getElementById('gameStatus');
        const currentPlayerElement = document.getElementById('currentPlayer');
        
        if (!statusElement || !currentPlayerElement) {
            console.warn('Status elements not found in DOM');
            return;
        }

        if (this.gameState.gameOver) {
            if (this.gameState.winner === 'Draw') {
                statusElement.textContent = "It's a draw!";
                statusElement.style.background = '#fef3c7';
                statusElement.style.borderLeftColor = '#f59e0b';
                statusElement.style.color = '#92400e';
            } else {
                statusElement.textContent = `${this.gameState.winner} wins!`;
                statusElement.style.background = '#dcfce7';
                statusElement.style.borderLeftColor = '#22c55e';
                statusElement.style.color = '#166534';
            }
            currentPlayerElement.textContent = 'Game Over';
        } else {
            statusElement.textContent = 'Game in progress...';
            statusElement.style.background = '#f0f9ff';
            statusElement.style.borderLeftColor = '#3182ce';
            statusElement.style.color = '#2c5282';
            currentPlayerElement.textContent = `Current Player: ${this.gameState.currentPlayer}`;
        }
    }

    updateControls() {
        if (!this.gameState) {
            console.warn('Game state not available for updateControls');
            return;
        }
        
        const aiMoveBtn = document.getElementById('aiMoveBtn');
        if (!aiMoveBtn) {
            console.warn('AI move button not found in DOM');
            return;
        }
        aiMoveBtn.disabled = this.gameState.gameOver || this.gameState.currentPlayer !== 'O';
        
        if (aiMoveBtn.disabled) {
            aiMoveBtn.style.opacity = '0.5';
            aiMoveBtn.style.cursor = 'not-allowed';
        } else {
            aiMoveBtn.style.opacity = '1';
            aiMoveBtn.style.cursor = 'pointer';
        }
    }

    updatePredictionDisplay() {
        const predictionDiv = document.getElementById('currentPrediction');
        if (!predictionDiv) {
            console.warn('Prediction display element not found in DOM');
            return;
        }
        
        if (!this.gameState) {
            predictionDiv.innerHTML = '<p class="text-gray-500">Loading game state...</p>';
            return;
        }
        
        if (this.gameState.prediction) {
            const prediction = this.gameState.prediction;
            predictionDiv.innerHTML = `
                <div class="prediction-item">
                    <i class="fas fa-gamepad"></i>
                    <span><strong>Game State:</strong> ${this.formatGameState(prediction.gameState)}</span>
                </div>
                <div class="prediction-item">
                    <i class="fas fa-brain"></i>
                    <span><strong>AI Prediction:</strong> ${prediction.prediction}</span>
                </div>
                <div class="prediction-item">
                    <i class="fas fa-percentage"></i>
                    <span><strong>Confidence:</strong> ${(prediction.confidence * 100).toFixed(1)}%</span>
                </div>
                <div class="prediction-item">
                    <i class="fas fa-robot"></i>
                    <span class="model-badge">${prediction.model}</span>
                </div>
            `;
        } else {
            predictionDiv.innerHTML = '<p class="text-gray-500">No prediction available</p>';
        }
    }

    updateStatsDisplay() {
        document.getElementById('gamesPlayed').textContent = this.stats.gamesPlayed;
        document.getElementById('totalPredictions').textContent = this.stats.predictionsTotal;
        
        const accuracy = this.stats.predictionsTotal > 0 
            ? ((this.stats.predictionsCorrect / this.stats.predictionsTotal) * 100).toFixed(1)
            : '0.0';
        document.getElementById('predictionAccuracy').textContent = `${accuracy}%`;
    }

    addToHistory(gameData) {
        if (!gameData.prediction) return;

        const historyItem = {
            timestamp: new Date().toISOString(),
            gameState: gameData.prediction.gameState,
            prediction: gameData.prediction.prediction,
            confidence: gameData.prediction.confidence,
            model: gameData.prediction.model,
            actualResult: gameData.winner || 'Unknown',
            isCorrect: gameData.winner === gameData.prediction.prediction
        };

        this.gameHistory.unshift(historyItem);
        
        // Keep only last 50 entries
        if (this.gameHistory.length > 50) {
            this.gameHistory = this.gameHistory.slice(0, 50);
        }

        // Update stats
        this.stats.predictionsTotal++;
        if (historyItem.isCorrect) {
            this.stats.predictionsCorrect++;
        }

        this.updateHistoryTable();
        this.updateStatsDisplay();
        this.saveGameHistory();
    }

    updateHistoryTable() {
        const tbody = document.getElementById('historyTableBody');
        
        if (this.gameHistory.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="no-data">No prediction history available</td></tr>';
            return;
        }

        tbody.innerHTML = this.gameHistory.map((item, index) => `
            <tr>
                <td>#${this.stats.predictionsTotal - index}</td>
                <td>
                    <span class="state-badge">${this.formatGameState(item.gameState)}</span>
                </td>
                <td>${item.prediction}</td>
                <td>${item.actualResult}</td>
                <td>
                    <span class="result-badge ${item.isCorrect ? 'correct' : 'incorrect'}">
                        ${item.isCorrect ? 'Correct' : 'Incorrect'}
                    </span>
                </td>
                <td>${(item.confidence * 100).toFixed(1)}%</td>
            </tr>
        `).join('');
    }

    clearHistory() {
        if (confirm('Are you sure you want to clear all prediction history?')) {
            this.gameHistory = [];
            this.stats.predictionsCorrect = 0;
            this.stats.predictionsTotal = 0;
            this.updateHistoryTable();
            this.updateStatsDisplay();
            this.saveGameHistory();
        }
    }

    clearPredictionDisplay() {
        document.getElementById('currentPrediction').innerHTML = 
            '<p class="text-gray-500">Make a move to see AI prediction</p>';
    }

    highlightWinningCombination() {
        // Define winning combinations
        const winCombinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
            [0, 4, 8], [2, 4, 6] // diagonals
        ];

        // Find the winning combination
        const board = this.gameState.board;
        const winner = this.gameState.winner;

        for (const combo of winCombinations) {
            if (combo.every(index => board[index] === winner)) {
                combo.forEach(index => {
                    document.querySelectorAll('.cell')[index].classList.add('winning');
                });
                break;
            }
        }
    }

    formatGameState(gameState) {
        if (!gameState || typeof gameState !== 'string') {
            return 'Unknown';
        }
        return gameState.replace(/,/g, ' ').toUpperCase();
    }

    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.display = show ? 'flex' : 'none';
        } else {
            console.warn('Loading overlay element not found in DOM');
        }
    }

    showError(message) {
        // Create a simple toast notification
        const toast = document.createElement('div');
        toast.className = 'error-toast';
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #fed7d7;
            color: #742a2a;
            padding: 15px 20px;
            border-radius: 10px;
            border: 1px solid #feb2b2;
            z-index: 1001;
            animation: slideInRight 0.3s ease-out;
        `;
        toast.textContent = message;

        document.body.appendChild(toast);

        // Remove toast after 3 seconds
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 3000);

        // Add CSS animations if not already added
        if (!document.getElementById('toast-animations')) {
            const style = document.createElement('style');
            style.id = 'toast-animations';
            style.textContent = `
                @keyframes slideInRight {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOutRight {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
    }

    saveGameHistory() {
        try {
            localStorage.setItem('tic-tac-toe-history', JSON.stringify({
                history: this.gameHistory,
                stats: this.stats
            }));
        } catch (error) {
            console.warn('Failed to save game history to localStorage:', error);
        }
    }

    loadGameHistory() {
        try {
            const saved = localStorage.getItem('tic-tac-toe-history');
            if (saved) {
                const data = JSON.parse(saved);
                this.gameHistory = data.history || [];
                this.stats = { ...this.stats, ...data.stats };
                this.updateHistoryTable();
                this.updateStatsDisplay();
            }
        } catch (error) {
            console.warn('Failed to load game history from localStorage:', error);
        }
    }
}

// Utility functions for enhanced UX
class UIEnhancements {
    static init() {
        this.addKeyboardShortcutsInfo();
        this.addTooltips();
        this.enableDarkModeToggle();
    }

    static addKeyboardShortcutsInfo() {
        // Add keyboard shortcuts info to the UI
        const gameControls = document.querySelector('.game-controls');
        if (gameControls && !document.getElementById('shortcutsInfo')) {
            const shortcutsDiv = document.createElement('div');
            shortcutsDiv.id = 'shortcutsInfo';
            shortcutsDiv.style.cssText = `
                margin-top: 15px;
                padding: 10px;
                background: #f8fafc;
                border-radius: 8px;
                font-size: 0.8rem;
                color: #718096;
                text-align: center;
            `;
            shortcutsDiv.innerHTML = `
                <strong>Keyboard Shortcuts:</strong> 
                Ctrl+R (Reset Game) | 
                Spacebar (AI Move)
            `;
            gameControls.appendChild(shortcutsDiv);
        }
    }

    static addTooltips() {
        // Add tooltips to buttons
        const tooltips = {
            'resetBtn': 'Start a new game (Ctrl+R)',
            'aiMoveBtn': 'Let AI make a move (Spacebar)',
            'clearHistoryBtn': 'Clear all prediction history'
        };

        Object.entries(tooltips).forEach(([id, text]) => {
            const element = document.getElementById(id);
            if (element) {
                element.title = text;
            }
        });
    }

    static enableDarkModeToggle() {
        // This could be extended to add dark mode functionality
        // For now, we'll just prepare the structure
        console.log('Dark mode toggle ready for implementation');
    }
}

// Performance optimization
class PerformanceOptimizer {
    static init() {
        this.debounceClicks();
        this.preloadImages();
    }

    static debounceClicks() {
        let lastClick = 0;
        document.addEventListener('click', (e) => {
            const now = Date.now();
            if (now - lastClick < 300) { // 300ms debounce
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
            lastClick = now;
        }, true);
    }

    static preloadImages() {
        // Preload any images that might be used later
        // Currently not needed, but structure is ready
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎮 Tic-Tac-Toe AI Game Initialized');
    
    // Initialize the main game
    const game = new TicTacToeGame();
    
    // Initialize UI enhancements
    UIEnhancements.init();
    
    // Initialize performance optimizations
    PerformanceOptimizer.init();
    
    // Make game globally accessible for debugging
    window.game = game;
    
    console.log('✅ All systems ready!');
});

// Service Worker registration for offline functionality (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}