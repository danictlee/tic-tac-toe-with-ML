class TicTacToeGame {
    constructor() {
        this.gameState = null;
        this.stats = {
            gamesPlayed: 0,
            predictionsTotal: 0,
            predictionsCorrect: 0
        };
        
        this.loadStats();
        this.initializeGame();
        this.setupEventListeners();
    }

    initializeGame() {
        this.loadGameState();
    }

    setupEventListeners() {
        // Game board clicks
        document.querySelectorAll('.cell').forEach((cell, index) => {
            cell.addEventListener('click', () => this.makeMove(index));
        });

        // Reset button
        const resetBtn = document.getElementById('resetBtn');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => this.resetGame());
        }

        // AI move button
        const aiMoveBtn = document.getElementById('aiMoveBtn');
        if (aiMoveBtn) {
            aiMoveBtn.addEventListener('click', () => this.makeAIMove());
        }
    }

    async loadGameState() {
        try {
            this.showLoading(true);
            const response = await fetch('/game_state');
            const data = await response.json();
            
            this.gameState = data;
            this.updateUI();
        } catch (error) {
            console.error('Error loading game state:', error);
            this.showError('Failed to load game state');
        } finally {
            this.showLoading(false);
        }
    }

    updateUI() {
        if (!this.gameState) {
            console.warn('Game state not available for UI update');
            return;
        }
        
        this.updateBoard();
        this.updateGameStatus();
        this.updateControls();
        this.updatePredictionDisplay();
        this.updateStatsDisplay();
    }

    async makeMove(position) {
        if (!this.gameState || this.gameState.gameOver || this.gameState.currentPlayer === 'O') {
            return;
        }

        try {
            this.showLoading(true);
            const response = await fetch('/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ position })
            });

            const data = await response.json();
            
            if (data.error) {
                this.showError(data.error);
                return;
            }

            this.gameState = data;
            this.updateUI();
            
            // Update stats if prediction was made
            if (data.prediction) {
                this.updateStats(data);
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
            
            // Update stats if prediction was made
            if (data.prediction) {
                this.updateStats(data);
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
            
            if (data.error) {
                this.showError(data.error);
                return;
            }

            this.gameState = data;
            this.updateUI();
            
            // Update games played counter
            this.stats.gamesPlayed++;
            this.saveStats();

        } catch (error) {
            console.error('Error resetting game:', error);
            this.showError('Failed to reset game');
        } finally {
            this.showLoading(false);
        }
    }

    updateBoard() {
        if (!this.gameState) {
            console.warn('Game state not available for board update');
            return;
        }
        
        const cells = document.querySelectorAll('.cell');
        cells.forEach((cell, index) => {
            const value = this.gameState.board[index];
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
                statusElement.className = 'game-status status-draw';
            } else {
                statusElement.textContent = `${this.gameState.winner} wins!`;
                statusElement.className = 'game-status status-won';
            }
            currentPlayerElement.textContent = 'Game Over';
        } else {
            statusElement.textContent = 'Game in progress...';
            statusElement.className = 'game-status status-playing';
            currentPlayerElement.textContent = `Current Player: ${this.gameState.currentPlayer}`;
        }
    }

    updateControls() {
        if (!this.gameState) return;
        
        const resetBtn = document.getElementById('resetBtn');
        const aiMoveBtn = document.getElementById('aiMoveBtn');
        
        if (resetBtn) {
            resetBtn.disabled = false;
        }
        
        if (aiMoveBtn) {
            aiMoveBtn.disabled = this.gameState.gameOver || this.gameState.currentPlayer !== 'O';
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
            
            // Basic information
            let html = `
                <div class="prediction-item">
                    <i class="fas fa-gamepad"></i>
                    <span><strong>Game State:</strong> ${this.formatGameState(prediction.gameState)}</span>
                </div>
                <div class="prediction-item">
                    <i class="fas fa-bullseye"></i>
                    <span><strong>Ground Truth:</strong> ${prediction.ground_truth}</span>
                </div>
            `;
            
            // Best model prediction (primary)
            html += `
                <div class="prediction-item primary-prediction">
                    <i class="fas fa-star"></i>
                    <span><strong>Best Model (${prediction.best_model}):</strong> ${prediction.best_prediction}</span>
                    <span class="confidence-badge">${(prediction.confidence * 100).toFixed(1)}%</span>
                </div>
            `;
            
            // All models comparison
            if (prediction.all_predictions && Object.keys(prediction.all_predictions).length > 0) {
                html += `<div class="models-comparison">
                    <h4>
                        <i class="fas fa-chart-bar"></i> All Models Comparison:
                    </h4>
                `;
                
                for (const [modelName, modelPrediction] of Object.entries(prediction.all_predictions)) {
                    const isCorrect = modelPrediction === prediction.ground_truth;
                    const isPrimary = modelName === prediction.best_model;
                    
                    html += `
                        <div class="model-prediction ${isPrimary ? 'primary-model' : ''} ${isCorrect ? 'correct-prediction' : ''}">
                            <span class="model-name">${modelName}</span>
                            <span class="model-result">${modelPrediction}</span>
                            ${isCorrect ? '<i class="fas fa-check-circle correct-icon"></i>' : '<i class="fas fa-times-circle incorrect-icon"></i>'}
                        </div>
                    `;
                }
                html += '</div>';
            }
            
            predictionDiv.innerHTML = html;
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

    updateStats(gameData) {
        if (!gameData.prediction) return;

        this.stats.predictionsTotal++;
        
        // Check if prediction was correct (comparing with ground truth)
        if (gameData.prediction.best_prediction === gameData.prediction.ground_truth) {
            this.stats.predictionsCorrect++;
        }

        this.updateStatsDisplay();
        this.saveStats();
    }

    formatGameState(gameState) {
        return gameState ? gameState.replace(/,/g, ' | ').replace(/_/g, '•') : 'Unknown';
    }

    highlightWinningCombination() {
        const winConditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
            [0, 4, 8], [2, 4, 6]              // Diagonals
        ];

        const cells = document.querySelectorAll('.cell');
        const board = this.gameState.board;

        for (const condition of winConditions) {
            if (board[condition[0]] === board[condition[1]] && 
                board[condition[1]] === board[condition[2]] && 
                board[condition[0]] !== '') {
                condition.forEach(index => {
                    cells[index].classList.add('winning');
                });
                break;
            }
        }
    }

    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.display = show ? 'flex' : 'none';
        }
    }

    showError(message) {
        // You could implement a proper error notification system here
        console.error('Game Error:', message);
        alert(`Error: ${message}`);
    }

    saveStats() {
        try {
            localStorage.setItem('ticTacToeStats', JSON.stringify(this.stats));
        } catch (error) {
            console.warn('Could not save stats to localStorage:', error);
        }
    }

    loadStats() {
        try {
            const saved = localStorage.getItem('ticTacToeStats');
            if (saved) {
                this.stats = { ...this.stats, ...JSON.parse(saved) };
            }
        } catch (error) {
            console.warn('Could not load stats from localStorage:', error);
        }
    }
}

// Initialize the game when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.ticTacToeGame = new TicTacToeGame();
});