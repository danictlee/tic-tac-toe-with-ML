from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import joblib
import os
import json

app = Flask(__name__)

# --- Load Model and Encoders ---
try:
    # Load the best model (primary)
    best_model = joblib.load('best_classifier.joblib')
    onehot_encoder = joblib.load('onehot_encoder.joblib')
    label_encoder = joblib.load('label_encoder.joblib')
    BEST_MODEL_NAME = type(best_model).__name__
    
    # Load other models for comparison
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.neural_network import MLPClassifier
    
    # Load training data to retrain other models
    print("Loading training data for other models...")
    train_df = pd.read_csv('train_dataset.csv')
    val_df = pd.read_csv('validation_dataset.csv')
    full_train_df = pd.concat([train_df, val_df])
    X_train = full_train_df.drop('target', axis=1)
    y_train = full_train_df['target']
    
    # Create other models with optimized parameters
    other_models = {
        'k-NN': KNeighborsClassifier(n_neighbors=5, weights='distance'),
        'Decision Tree': DecisionTreeClassifier(max_depth=10, min_samples_split=2, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42)
    }
    
    # Train other models
    print("Training models for comparison...")
    for name, model in other_models.items():
        model.fit(X_train, y_train)
    
    # Add the best model to the dictionary
    if isinstance(best_model, MLPClassifier):
        other_models['MLP'] = best_model
    elif isinstance(best_model, KNeighborsClassifier):
        other_models['k-NN'] = best_model
    elif isinstance(best_model, DecisionTreeClassifier):
        other_models['Decision Tree'] = best_model
    elif isinstance(best_model, RandomForestClassifier):
        other_models['Random Forest'] = best_model
    
    print(f"✅ Primary model loaded: {BEST_MODEL_NAME}")
    print(f"✅ All models loaded: {list(other_models.keys())}")
    
except FileNotFoundError as e:
    print("❌ Error: Model files not found. Please run notebooks 01 and 02 first.")
    print(f"Missing file: {e}")
except Exception as e:
    print(f"❌ Error loading models: {e}")

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
        """AI makes a random available move"""
        if self.game_over or self.current_player != 'O':
            return False
            
        # Find all available moves
        available_moves = [i for i, cell in enumerate(self.board) if cell == '']
        if available_moves:
            # Choose random position instead of always first
            import random
            position = random.choice(available_moves)
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
        """Get AI prediction with all models"""
        try:
            # Convert board to format expected by ML model
            mapping = {'X': 1, 'O': 0, '': 2}
            flat_board_numeric = [mapping[cell] for cell in self.board]
            columns = ['A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'C3']
            board_df = pd.DataFrame([flat_board_numeric], columns=columns)
            board_onehot = onehot_encoder.transform(board_df)
            
            # Get predictions from all models
            all_predictions = {}
            for model_name, model in other_models.items():
                prediction_encoded = model.predict(board_onehot)
                prediction_label = label_encoder.inverse_transform(prediction_encoded)[0]
                all_predictions[model_name] = prediction_label
            
            # Get best model prediction and confidence
            best_prediction_encoded = best_model.predict(board_onehot)
            best_prediction_proba = best_model.predict_proba(board_onehot)
            best_prediction = label_encoder.inverse_transform(best_prediction_encoded)[0]
            confidence = float(np.max(best_prediction_proba))
            
            # Get ground truth
            ground_truth = self.get_board_state_ground_truth()
            
            # Format board state for display
            board_state_str = ','.join([cell if cell != '' else '_' for cell in self.board])
            
            return {
                'best_prediction': best_prediction,
                'all_predictions': all_predictions,
                'ground_truth': ground_truth,
                'confidence': confidence,
                'gameState': board_state_str,
                'best_model': BEST_MODEL_NAME
            }
        except Exception as e:
            print(f"Error in AI prediction: {e}")
            return {
                'best_prediction': 'Error',
                'all_predictions': {},
                'ground_truth': 'Error',
                'confidence': 0.0,
                'gameState': 'Unknown',
                'best_model': BEST_MODEL_NAME
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
        'totalMoves': game.total_moves,
        'correctPredictions': game.correct_predictions,
        'accuracy': (game.correct_predictions / max(game.total_moves, 1)) * 100,
        'prediction': game.last_prediction
    })

@app.route('/move', methods=['POST'])
def make_move():
    """Make a move on the board"""
    data = request.json
    position = data.get('position')
    
    if position is None or not (0 <= position <= 8):
        return jsonify({'error': 'Invalid position'}), 400
    
    success = game.make_move(position)
    
    if not success:
        return jsonify({'error': 'Invalid move'}), 400
    
    return jsonify({
        'board': game.board,
        'currentPlayer': game.current_player,
        'gameOver': game.game_over,
        'winner': game.winner,
        'totalMoves': game.total_moves,
        'correctPredictions': game.correct_predictions,
        'accuracy': (game.correct_predictions / max(game.total_moves, 1)) * 100,
        'prediction': game.last_prediction
    })

@app.route('/reset', methods=['POST'])
def reset_game():
    """Reset the game"""
    game.reset_game()
    return jsonify({
        'board': game.board,
        'currentPlayer': game.current_player,
        'gameOver': game.game_over,
        'winner': game.winner,
        'totalMoves': game.total_moves,
        'correctPredictions': game.correct_predictions,
        'accuracy': 0,
        'prediction': None
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
    print(f"📊 Using primary model: {BEST_MODEL_NAME}")
    print(f"🔍 Comparison models: {list(other_models.keys())}")
    print("🌐 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
