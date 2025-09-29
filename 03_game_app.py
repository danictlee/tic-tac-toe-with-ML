import numpy as np
import pandas as pd
import random
import joblib
import os

# --- Carregar Modelos e Encoders ---
try:
    onehot_encoder = joblib.load('posicoes_encoder.joblib')
    label_encoder = joblib.load('classes_encoder.joblib')

    # Carregar todos os modelos individuais
    model_files = {
        'k-NN': 'knn_model.joblib',
        'Decision Tree': 'dt_model.joblib',
        'Random Forest': 'rf_model.joblib',
        'MLP': 'mlp_model.joblib'
    }
    models = {name: joblib.load(fname) for name, fname in model_files.items()}

    print(f"Modelos carregados: {list(models.keys())}")

except FileNotFoundError:
    print("Erro: Arquivos de modelo (.joblib) ou encoders não encontrados.")
    print("Por favor, execute os notebooks 01 e 02 primeiro.")
    exit()
except Exception as e:
    print(f"Erro ao carregar modelos: {e}")
    exit()

# --- Funções do Jogo e da IA ---
def print_board(board):
    """Imprime o tabuleiro do jogo da velha"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n  Jogo da Velha - IA Analisando")
    print("-------------")
    for i in range(3):
        row_display = []
        for j in range(3):
            pos_num = 3 * i + j + 1
            row_display.append(board[i][j] if board[i][j] != ' ' else str(pos_num))
        print(f"|  {row_display[0]}  |  {row_display[1]}  |  {row_display[2]}  |")
        print("-------------")

def get_board_state_ground_truth(board):
    """Determina o estado real do jogo baseado nas regras"""
    board_flat = [cell for row in board for cell in row if cell != ' ']
    board_positions = [cell if cell != ' ' else None for row in board for cell in row]
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
        [0, 4, 8], [2, 4, 6]              # Diagonais
    ]

    for player in ['x', 'o']:
        for condition in win_conditions:
            if all(board_positions[i] == player for i in condition):
                return 'Fim de Jogo'
    if None not in board_positions:
        return 'Fim de Jogo'
    for player in ['x', 'o']:
        for condition in win_conditions:
            line = [board_positions[i] for i in condition]
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

def get_ai_predictions_all_models(board):
    """Obtém as predições de todos os modelos para o estado atual do tabuleiro"""
    processed_board = preprocess_board_for_model(board)
    predictions = {}
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="X does not have valid feature names")
        for model_name, model in models.items():
            prediction_encoded = model.predict(processed_board)
            prediction_label = label_encoder.inverse_transform(prediction_encoded)[0]
            predictions[model_name] = prediction_label
    return predictions

class TicTacToeAI:
    """Classe que engloba toda a funcionalidade do jogo da velha com análise de IA."""

    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'x'
        self.game_history = []

    def reset_game(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'x'
        self.game_history = []

    def is_valid_move(self, row, col):
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' '

    def make_move(self, row, col):
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            return True
        return False

    def switch_player(self):
        self.current_player = 'o' if self.current_player == 'x' else 'x'

    def get_board_state(self):
        return [cell for row in self.board for cell in row]

    def get_ai_analysis(self):
        all_predictions = get_ai_predictions_all_models(self.board)
        ground_truth = get_board_state_ground_truth(self.board)
        analysis = {
            'all_predictions': all_predictions,
            'ground_truth': ground_truth,
            'board_state': self.get_board_state()
        }
        return analysis

    def make_ai_move(self):
        available_moves = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ' ']
        if available_moves:
            row, col = random.choice(available_moves)
            self.board[row][col] = 'o'
            return True
        return False

def game_loop():
    game = TicTacToeAI()
    print(f"\n🎯 Jogo da Velha com Análise de IA")
    print(f"🔍 Modelos disponíveis: {', '.join(models.keys())}")
    print("\n📝 Como jogar:")
    print("- Digite números de 1 a 9 para escolher uma posição")
    print("- O tabuleiro mostra os números disponíveis")
    print("- A IA analisa cada estado do jogo com TODOS os modelos")
    print("- O computador (O) escolhe posições aleatórias\n")

    while True:
        print_board(game.board)
        analysis = game.get_ai_analysis()
        print(f"\n🎯 ANÁLISE COMPLETA DA IA:")
        print(f"📍 Estado Real (Ground Truth): {analysis['ground_truth']}")
        print(f"\n📊 PREDIÇÕES DE TODOS OS MODELOS:")
        for model_name, prediction in analysis['all_predictions'].items():
            match_status = "✓ CORRETO" if prediction == analysis['ground_truth'] else "✗ INCORRETO"
            print(f"   {model_name:15} → {prediction:20} ({match_status})")

        if analysis['ground_truth'] == 'Fim de Jogo':
            print("\n🎉 Jogo finalizado!")
            break

        if game.current_player == 'x':
            try:
                position = int(input(f"\nJogador {game.current_player.upper()}, escolha sua posição (1-9): "))
                if position < 1 or position > 9:
                    print("❌ Posição inválida! Digite um número entre 1 e 9.")
                    continue
                row = (position - 1) // 3
                col = (position - 1) % 3
                if game.make_move(row, col):
                    game.switch_player()
                else:
                    print("❌ Posição já ocupada! Escolha outra.")
            except ValueError:
                print("❌ Digite apenas números!")
        else:
            print("\n🎲 Computador escolhendo posição aleatória...")
            import time
            time.sleep(1)
            if game.make_ai_move():
                print("✅ Computador escolheu sua posição!")
                game.switch_player()
            else:
                print("❌ Erro: Computador não conseguiu escolher posição.")
                break

    while True:
        play_again = input("\n🎮 Jogar novamente? (s/n): ").lower().strip()
        if play_again in ['s', 'sim', 'y', 'yes']:
            game.reset_game()
            game_loop()
            break
        elif play_again in ['n', 'não', 'nao', 'no']:
            print("\n👋 Obrigado por jogar!")
            break
        else:
            print("❓ Digite 's' para sim ou 'n' para não.")

if __name__ == "__main__":
    print("=== Jogo da Velha com IA Multi-Modelo ===")
    print("Você joga como 'x' e o computador como 'o'")
    print("A IA irá analisar o estado do jogo com TODOS os modelos treinados!")
    print("O computador escolhe posições aleatórias (não joga estrategicamente)")
    input("Pressione Enter para começar...")
    game_loop()