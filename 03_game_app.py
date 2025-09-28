import numpy as np
import pandas as pd
import random
import joblib
import os

# --- Load Model and Encoders ---
try:
    model = joblib.load('best_classifier.joblib')
    onehot_encoder = joblib.load('onehot_encoder.joblib')
    label_encoder = joblib.load('label_encoder.joblib')
    MODEL_NAME = type(model).__name__
except FileNotFoundError:
    print("Error: Model files ('best_classifier.joblib') or encoders not found.")
    print("Please run notebooks 01 and 02 first.")
    exit()

# --- Game and AI Functions ---
def print_board(board):
    """Prints the tic-tac-toe board"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n  Tic-Tac-Toe - AI Analyzing")
    print("-------------")
    # Print board replacing ' ' with position numbers
    for i in range(3):
        row_display = []
        for j in range(3):
            pos_num = 3 * i + j + 1
            row_display.append(board[i][j] if board[i][j] != ' ' else str(pos_num))
        print(f"|  {row_display[0]}  |  {row_display[1]}  |  {row_display[2]}  |")
        print("-------------")

def get_board_state_ground_truth(board):
    """Determines the real game state based on rules"""
    board_flat = [cell if cell != ' ' else None for row in board for cell in row]
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]

    # Check if someone won
    for player in ['x', 'o']:
        for condition in win_conditions:
            if all(board_flat[i] == player for i in condition):
                return 'Fim de Jogo'
    
    # Check draw
    if None not in board_flat:
        return 'Fim de Jogo'

    # Check possibility of end (someone can win next move)
    for player in ['x', 'o']:
        for condition in win_conditions:
            line = [board_flat[i] for i in condition]
            if line.count(player) == 2 and line.count(None) == 1:
                return 'Possibilidade de Fim'

    return 'Tem Jogo'

def preprocess_board_for_model(board):
    """Converts board to format expected by model"""
    mapping = {'x': 1, 'o': 0, ' ': 2}
    flat_board_numeric = [mapping[cell] for row in board for cell in row]
    columns = ['A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'C3']
    board_df = pd.DataFrame([flat_board_numeric], columns=columns)
    board_onehot = onehot_encoder.transform(board_df)
    return board_onehot

def get_ai_prediction(board):
    """Gets AI prediction for current board state"""
    processed_board = preprocess_board_for_model(board)
    prediction_encoded = model.predict(processed_board)
    prediction_label = label_encoder.inverse_transform(prediction_encoded)[0]
    return prediction_label

# --- Main Game Loop ---
def game_loop():
    """Main game loop"""
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'x'
    total_moves = 0
    correct_predictions = 0

    while True:
        print_board(board)
        
        # AI analysis (only after first move)
        if total_moves > 0:
            real_state = get_board_state_ground_truth(board)
            ai_prediction = get_ai_prediction(board)
            is_correct = (real_state == ai_prediction)
            if is_correct:
                correct_predictions += 1
            
            print(f"\n--- AI Analysis ({MODEL_NAME}) ---")
            print(f"Real Game State (Verifier): {real_state}")
            print(f"AI Prediction: {ai_prediction}")
            print(f"The prediction is {'CORRECT' if is_correct else 'INCORRECT'}")
            accuracy = (correct_predictions / total_moves) * 100 if total_moves > 0 else 0
            print(f"Real-time accuracy: {accuracy:.2f}% ({correct_predictions}/{total_moves})")
            
            # Check game end
            if real_state == 'Fim de Jogo':
                # Check who won
                board_flat = [cell for row in board for cell in row]
                winner = None
                win_conditions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
                
                for p in ['x', 'o']:
                    for cond in win_conditions:
                        if all(board_flat[i] == p for i in cond):
                            winner = p
                            break
                    if winner:
                        break
                
                print_board(board)  # Show final board
                if winner:
                    print(f"\nGAME OVER! Player '{winner}' wins!")
                else:
                    print("\nGAME OVER! It's a draw!")
                break

        # Turn Logic
        if current_player == 'x':  # Human Player
            try:
                move_str = input(f"\nPlayer '{current_player}' turn. Choose a position (1-9): ")
                if not move_str.isdigit(): 
                    raise ValueError
                move = int(move_str)
                if move < 1 or move > 9: 
                    raise ValueError
                row, col = (move - 1) // 3, (move - 1) % 3
                if board[row][col] == ' ':
                    board[row][col] = current_player
                    total_moves += 1
                    current_player = 'o'
                else:
                    print("Position already occupied. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a number from 1 to 9.")
        
        else:  # Computer Player (Random)
            print(f"\nComputer turn ('{current_player}')...")
            empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']
            if empty_cells:
                row, col = random.choice(empty_cells)
                board[row][col] = current_player
                total_moves += 1
                current_player = 'x'
                input("Press Enter to continue...")

if __name__ == "__main__":
    print("=== Tic-Tac-Toe with AI ===")
    print("You play as 'x' and the computer as 'o'")
    print("The AI will analyze the game state at each move!")
    input("Press Enter to start...")
    game_loop()