import numpy as np
import pandas as pd
import random
import joblib
import os

# --- Carregar Modelo e Encoders ---
try:
    model = joblib.load('best_classifier.joblib')
    onehot_encoder = joblib.load('onehot_encoder.joblib')
    label_encoder = joblib.load('label_encoder.joblib')
    MODEL_NAME = type(model).__name__
except FileNotFoundError:
    print("Erro: Arquivos de modelo ('best_classifier.joblib') ou encoders não encontrados.")
    print("Por favor, execute os notebooks 01 e 02 primeiro.")
    exit()

# --- Funções do Jogo e da IA ---
def print_board(board):
    """Imprime o tabuleiro do jogo da velha"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n  Jogo da Velha - IA Analisando")
    print("-------------")
    # Imprime o tabuleiro substituindo ' ' pelos números das posições
    for i in range(3):
        row_display = []
        for j in range(3):
            pos_num = 3 * i + j + 1
            row_display.append(board[i][j] if board[i][j] != ' ' else str(pos_num))
        print(f"|  {row_display[0]}  |  {row_display[1]}  |  {row_display[2]}  |")
        print("-------------")

def get_board_state_ground_truth(board):
    """Determina o estado real do jogo baseado nas regras"""
    board_flat = [cell if cell != ' ' else None for row in board for cell in row]
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
        [0, 4, 8], [2, 4, 6]              # Diagonais
    ]

    # Verifica se alguém ganhou
    for player in ['x', 'o']:
        for condition in win_conditions:
            if all(board_flat[i] == player for i in condition):
                return 'Fim de Jogo'
    
    # Verifica empate
    if None not in board_flat:
        return 'Fim de Jogo'

    # Verifica possibilidade de fim (alguém pode ganhar na próxima jogada)
    for player in ['x', 'o']:
        for condition in win_conditions:
            line = [board_flat[i] for i in condition]
            if line.count(player) == 2 and line.count(None) == 1:
                return 'Possibilidade de Fim'

    return 'Tem Jogo'

def preprocess_board_for_model(board):
    """Converte o tabuleiro para o formato esperado pelo modelo"""
    mapping = {'x': 1, 'o': 0, ' ': 2}
    flat_board_numeric = [mapping[cell] for row in board for cell in row]
    columns = ['A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'C3']
    board_df = pd.DataFrame([flat_board_numeric], columns=columns)
    board_onehot = onehot_encoder.transform(board_df)
    return board_onehot

def get_ai_prediction(board):
    """Obtém a predição da IA para o estado atual do tabuleiro"""
    processed_board = preprocess_board_for_model(board)
    prediction_encoded = model.predict(processed_board)
    prediction_label = label_encoder.inverse_transform(prediction_encoded)[0]
    return prediction_label

# --- Loop Principal do Jogo ---
def game_loop():
    """Loop principal do jogo"""
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'x'
    total_moves = 0
    correct_predictions = 0

    while True:
        print_board(board)
        
        # Análise da IA (apenas após a primeira jogada)
        if total_moves > 0:
            real_state = get_board_state_ground_truth(board)
            ai_prediction = get_ai_prediction(board)
            is_correct = (real_state == ai_prediction)
            if is_correct:
                correct_predictions += 1
            
            print(f"\n--- Análise da IA ({MODEL_NAME}) ---")
            print(f"Estado Real do Jogo (Verificador): {real_state}")
            print(f"Predição da IA: {ai_prediction}")
            print(f"A predição está {'CORRETA' if is_correct else 'INCORRETA'}")
            accuracy = (correct_predictions / total_moves) * 100 if total_moves > 0 else 0
            print(f"Acurácia em tempo real: {accuracy:.2f}% ({correct_predictions}/{total_moves})")
            
            # Verifica fim de jogo
            if real_state == 'Fim de Jogo':
                # Verifica quem ganhou
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
                
                print_board(board)  # Mostra o tabuleiro final
                if winner:
                    print(f"\nFIM DE JOGO! O jogador '{winner}' venceu!")
                else:
                    print("\nFIM DE JOGO! Deu empate!")
                break

        # Lógica de Turnos
        if current_player == 'x':  # Jogador Humano
            try:
                move_str = input(f"\nTurno do Jogador '{current_player}'. Escolha uma posição (1-9): ")
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
                    print("Posição já ocupada. Tente novamente.")
            except (ValueError, IndexError):
                print("Entrada inválida. Por favor, insira um número de 1 a 9.")
        
        else:  # Jogador Computador (Aleatório)
            print(f"\nTurno do Computador ('{current_player}')...")
            empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']
            if empty_cells:
                row, col = random.choice(empty_cells)
                board[row][col] = current_player
                total_moves += 1
                current_player = 'x'
                input("Pressione Enter para continuar...")

if __name__ == "__main__":
    print("=== Jogo da Velha com IA ===")
    print("Você joga como 'x' e o computador como 'o'")
    print("A IA irá analisar o estado do jogo a cada movimento!")
    input("Pressione Enter para começar...")
    game_loop()