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
    board_flat = [cell for row in board for cell in row if cell != ' ']
    board_positions = [cell if cell != ' ' else None for row in board for cell in row]
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
        [0, 4, 8], [2, 4, 6]              # Diagonais
    ]

    # Verifica se alguém ganhou
    for player in ['x', 'o']:
        for condition in win_conditions:
            if all(board_positions[i] == player for i in condition):
                return 'Fim de Jogo'
    
    # Verifica empate
    if None not in board_positions:
        return 'Fim de Jogo'

    # Verifica possibilidade de fim (alguém pode ganhar na próxima jogada)
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

def get_ai_prediction(board):
    """Obtém a predição da IA para o estado atual do tabuleiro"""
    processed_board = preprocess_board_for_model(board)
    prediction_encoded = model.predict(processed_board)
    prediction_label = label_encoder.inverse_transform(prediction_encoded)[0]
    return prediction_label

class TicTacToeAI:
    """Classe que engloba toda a funcionalidade do jogo da velha com análise de IA."""
    
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'x'
        self.game_history = []
    
    def reset_game(self):
        """Reinicia o jogo"""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'x'
        self.game_history = []
    
    def is_valid_move(self, row, col):
        """Verifica se um movimento é válido"""
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' '
    
    def make_move(self, row, col):
        """Executa um movimento"""
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            return True
        return False
    
    def switch_player(self):
        """Troca o jogador atual"""
        self.current_player = 'o' if self.current_player == 'x' else 'x'
    
    def get_board_state(self):
        """Retorna o estado do tabuleiro como lista plana"""
        return [cell for row in self.board for cell in row]
    
    def get_ai_analysis(self):
        """Obtém análise da IA para o estado atual"""
        prediction = get_ai_prediction(self.board)
        ground_truth = get_board_state_ground_truth(self.board)
        
        analysis = {
            'ai_prediction': prediction,
            'ground_truth': ground_truth,
            'model_name': MODEL_NAME,
            'board_state': self.get_board_state()
        }
        
        return analysis

def game_loop():
    """Loop principal do jogo"""
    game = TicTacToeAI()
    print(f"\n🎯 Jogo da Velha com Análise de IA")
    print(f"📊 Modelo utilizado: {MODEL_NAME}")
    print("\n📝 Como jogar:")
    print("- Digite números de 1 a 9 para escolher uma posição")
    print("- O tabuleiro mostra os números disponíveis")
    print("- A IA analisa cada estado do jogo\n")
    
    while True:
        print_board(game.board)
        
        # Análise da IA
        analysis = game.get_ai_analysis()
        print(f"\n🤖 Análise da IA ({MODEL_NAME}):")
        print(f"   Predição: {analysis['ai_prediction']}")
        print(f"   Realidade: {analysis['ground_truth']}")
        
        # Verifica se o jogo acabou
        if analysis['ground_truth'] == 'Fim de Jogo':
            print("\n🎉 Jogo finalizado!")
            break
        
        # Entrada do jogador
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
    
    # Pergunta se quer jogar novamente
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
    print("=== Jogo da Velha com IA ===")
    print("Você joga como 'x' e o computador como 'o'")
    print("A IA irá analisar o estado do jogo a cada movimento!")
    input("Pressione Enter para começar...")
    game_loop()