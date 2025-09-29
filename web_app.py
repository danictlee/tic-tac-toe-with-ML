from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import joblib
import os
import json

app = Flask(__name__)

# --- Load Model and Encoders ---
try:
    model = joblib.load('best_classifier.joblib')
    onehot_encoder = joblib.load('onehot_encoder.joblib')
    label_encoder = joblib.load('label_encoder.joblib')
    MODEL_NAME = type(model).__name__
    print(f"✅ Model loaded successfully: {MODEL_NAME}")
except FileNotFoundError as e:
    print("❌ Error: Model files not found. Please run notebooks 01 and 02 first.")
    print(f"Missing file: {e}")

class TicTacToeAI:
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        """Reset the game state"""
        self.board = [''] * 9  # Flat representation: 0-8 positions
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.total_moves = 0
        self.correct_predictions = 0
        self.predictions_history = []
        self.last_prediction = None
    
    def make_move(self, position):
        """Make a move on the board at given position (0-8)"""
        if self.board[position] == '' and not self.game_over:
            self.board[position] = self.current_player
            self.total_moves += 1
            
            # Get AI prediction before checking game end
            ai_prediction_result = self.get_ai_prediction()
            self.last_prediction = ai_prediction_result
            
            # Check if game ended
            self.check_game_end()
            
            # Switch player if game continues
            if not self.game_over:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            
            return True
        return False
    
    def make_ai_move(self):
        """AI makes the best available move"""
        if self.game_over or self.current_player != 'O':
            return False
            
        # Find best move (simple strategy for now)
        available_moves = [i for i, cell in enumerate(self.board) if cell == '']
        if available_moves:
            # For demo purposes, pick first available move
            # In a real implementation, this would use minimax or other AI strategy
            position = available_moves[0]
            return self.make_move(position)
        return False

    def check_game_end(self):
        """Check if the game has ended and set winner"""
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]

        # Check for winner
        for condition in win_conditions:
            if (self.board[condition[0]] == self.board[condition[1]] == 
                self.board[condition[2]] != ''):
                self.game_over = True
                self.winner = self.board[condition[0]]
                return
        
        # Check for draw
        if '' not in self.board:
            self.game_over = True
            self.winner = 'Draw'
            return
    
    def get_board_state_ground_truth(self):
        """Determine the current state of the board for ML prediction"""
        board_for_ml = [cell.lower() if cell != '' else ' ' for cell in self.board]
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]

        # Check if someone won
        for player in ['x', 'o']:
            for condition in win_conditions:
                if all(board_for_ml[i] == player for i in condition):
                    return 'Fim de Jogo'
        
        # Check draw
        if ' ' not in board_for_ml:
            return 'Fim de Jogo'

        # Check possibility of end (someone can win next move)
        for player in ['x', 'o']:
            for condition in win_conditions:
                line = [board_for_ml[i] for i in condition]
                if line.count(player) == 2 and line.count(' ') == 1:
                    return 'Possibilidade de Fim'

        return 'Tem Jogo'
    
    def get_ai_prediction(self):
        """Get AI prediction for current board state"""
        try:
            # Convert board to format expected by ML model
            mapping = {'X': 1, 'O': 0, '': 2}
            flat_board_numeric = [mapping[cell] for cell in self.board]
            columns = ['A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'C3']
            board_df = pd.DataFrame([flat_board_numeric], columns=columns)
            board_onehot = onehot_encoder.transform(board_df)
            
            prediction_encoded = model.predict(board_onehot)
            prediction_proba = model.predict_proba(board_onehot)
            prediction_label = label_encoder.inverse_transform(prediction_encoded)[0]
            confidence = np.max(prediction_proba)
            
            # Format board state for display
            board_state_str = ','.join([cell if cell != '' else '_' for cell in self.board])
            
            return {
                'prediction': prediction_label,
                'confidence': float(confidence),
                'gameState': board_state_str,
                'model': MODEL_NAME
            }
        except Exception as e:
            print(f"Error in AI prediction: {e}")
            return {
                'prediction': 'Error',
                'confidence': 0.0,
                'gameState': 'Unknown',
                'model': MODEL_NAME
            }

# Global game instance
game = TicTacToeAI()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/game_state')
def get_game_state():
    """Get current game state"""
    return jsonify({
        'board': game.board,
        'currentPlayer': game.current_player,
        'gameOver': game.game_over,
        'winner': game.winner,
        'prediction': game.last_prediction
    })

@app.route('/reset', methods=['POST'])
def reset_game():
    """Reset the game"""
    global game
    game.reset_game()
    return jsonify({
        'board': game.board,
        'currentPlayer': game.current_player,
        'gameOver': game.game_over,
        'winner': game.winner,
        'prediction': None
    })

@app.route('/move', methods=['POST'])
def make_move():
    """Make a move"""
    data = request.json
    position = data.get('position')
    
    if position is None:
        return jsonify({'error': 'Position is required'}), 400
    
    success = game.make_move(position)
    
    if not success:
        return jsonify({'error': 'Invalid move'}), 400
    
    return jsonify({
        'board': game.board,
        'currentPlayer': game.current_player,
        'gameOver': game.game_over,
        'winner': game.winner,
        'prediction': game.last_prediction
    })

@app.route('/ai_move', methods=['POST'])
def ai_move():
    """Make an AI move"""
    success = game.make_ai_move()
    
    if not success:
        return jsonify({'error': 'AI cannot make a move'}), 400
    
    return jsonify({
        'board': game.board,
        'currentPlayer': game.current_player,
        'gameOver': game.game_over,
        'winner': game.winner,
        'prediction': game.last_prediction
    })

if __name__ == '__main__':
    print("🚀 Starting Tic-Tac-Toe AI Web Application...")
    print(f"📊 Using model: {MODEL_NAME}")
    print("🌐 Open your browser to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)