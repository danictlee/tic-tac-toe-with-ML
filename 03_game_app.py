import numpy as np
import pandas as pd
import random
import joblib
import os

# --- Carregar Modelo e Encoders ---
try:
    # Carregar o melhor modelo (principal)
    best_model = joblib.load('best_classifier.joblib')
    onehot_encoder = joblib.load('onehot_encoder.joblib')
    label_encoder = joblib.load('label_encoder.joblib')
    BEST_MODEL_NAME = type(best_model).__name__
    
    # Carregar todos os outros modelos para comparação
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.neural_network import MLPClassifier
    
    # Recriar e treinar os outros modelos com os melhores parâmetros encontrados
    print("Carregando dados de treino para outros modelos...")
    train_df = pd.read_csv('train_dataset.csv')
    val_df = pd.read_csv('validation_dataset.csv')
    full_train_df = pd.concat([train_df, val_df])
    X_train = full_train_df.drop('target', axis=1)
    y_train = full_train_df['target']
    
    # Criar outros modelos com parâmetros otimizados
    other_models = {
        'k-NN': KNeighborsClassifier(n_neighbors=5, weights='distance'),
        'Decision Tree': DecisionTreeClassifier(max_depth=10, min_samples_split=2, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42)
    }
    
    # Treinar os outros modelos
    print("Treinando modelos para comparação...")
    for name, model in other_models.items():
        model.fit(X_train, y_train)
    
    # Adicionar o melhor modelo ao dicionário
    if isinstance(best_model, MLPClassifier):
        other_models['MLP'] = best_model
    elif isinstance(best_model, KNeighborsClassifier):
        other_models['k-NN'] = best_model
    elif isinstance(best_model, DecisionTreeClassifier):
        other_models['Decision Tree'] = best_model
    elif isinstance(best_model, RandomForestClassifier):
        other_models['Random Forest'] = best_model
    
    print(f"Modelo principal: {BEST_MODEL_NAME}")
    print(f"Modelos carregados: {list(other_models.keys())}")
    
except FileNotFoundError:
    print("Erro: Arquivos de modelo ('best_classifier.joblib') ou encoders não encontrados.")
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

def get_ai_predictions_all_models(board):
    """Obtém as predições de todos os modelos para o estado atual do tabuleiro"""
    processed_board = preprocess_board_for_model(board)
    predictions = {}
    
    # Suppress sklearn warnings about feature names
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="X does not have valid feature names")
        
        for model_name, model in other_models.items():
            prediction_encoded = model.predict(processed_board)
            prediction_label = label_encoder.inverse_transform(prediction_encoded)[0]
            predictions[model_name] = prediction_label
    
    return predictions

def get_ai_prediction(board):
    """Obtém a predição do melhor modelo (compatibilidade)"""
    processed_board = preprocess_board_for_model(board)
    
    # Suppress sklearn warnings about feature names
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="X does not have valid feature names")
        prediction_encoded = best_model.predict(processed_board)
    
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
        """Obtém análise da IA para o estado atual com todos os modelos"""
        all_predictions = get_ai_predictions_all_models(self.board)
        best_prediction = get_ai_prediction(self.board)
        ground_truth = get_board_state_ground_truth(self.board)
        
        analysis = {
            'best_prediction': best_prediction,
            'all_predictions': all_predictions,
            'ground_truth': ground_truth,
            'best_model_name': BEST_MODEL_NAME,
            'board_state': self.get_board_state()
        }
        
        return analysis
    
    def make_ai_move(self):
        """Faz o computador escolher uma posição aleatória disponível"""
        # Encontra todas as posições disponíveis
        available_moves = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ' ']
        
        if available_moves:
            # Escolhe aleatoriamente uma das posições disponíveis
            row, col = random.choice(available_moves)
            self.board[row][col] = 'o'
            return True
        
        return False

def game_loop():
    """Loop principal do jogo"""
    game = TicTacToeAI()
    print(f"\n🎯 Jogo da Velha com Análise de IA")
    print(f"📊 Modelo principal: {BEST_MODEL_NAME}")
    print(f"🔍 Modelos para comparação: {', '.join(other_models.keys())}")
    print("\n📝 Como jogar:")
    print("- Digite números de 1 a 9 para escolher uma posição")
    print("- O tabuleiro mostra os números disponíveis")
    print("- A IA analisa cada estado do jogo com TODOS os modelos")
    print("- O computador (O) escolhe posições aleatórias\n")
    
    while True:
        print_board(game.board)
        
        # Análise da IA com todos os modelos
        analysis = game.get_ai_analysis()
        print(f"\n🎯 ANÁLISE COMPLETA DA IA:")
        print(f"📍 Estado Real (Ground Truth): {analysis['ground_truth']}")
        print(f"\n🏆 PREDIÇÃO DO MODELO PRINCIPAL ({BEST_MODEL_NAME}): {analysis['best_prediction']}")
        print(f"\n📊 COMPARAÇÃO COM TODOS OS MODELOS:")
        
        # Mostrar predições de todos os modelos
        for model_name, prediction in analysis['all_predictions'].items():
            status = "✅ PRINCIPAL" if model_name == BEST_MODEL_NAME else "📋 Comparação"
            match_status = "✓ CORRETO" if prediction == analysis['ground_truth'] else "✗ INCORRETO"
            print(f"   {status} {model_name:15} → {prediction:20} ({match_status})")
        
        # Verifica se o jogo acabou
        if analysis['ground_truth'] == 'Fim de Jogo':
            print("\n🎉 Jogo finalizado!")
            break
        
        # Turno do jogador humano (X)
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
        
        # Turno do computador (O) - escolha aleatória
        else:
            print("\n🎲 Computador escolhendo posição aleatória...")
            import time
            time.sleep(1)  # Pequena pausa para dramaticidade
            
            if game.make_ai_move():
                print("✅ Computador escolheu sua posição!")
                game.switch_player()
            else:
                print("❌ Erro: Computador não conseguiu escolher posição.")
                break
    
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
    print("=== Jogo da Velha com IA Multi-Modelo ===")
    print(f"Modelo principal: {BEST_MODEL_NAME}")
    print("Você joga como 'x' e o computador como 'o'")
    print("A IA irá analisar o estado do jogo com TODOS os modelos treinados!")
    print("O computador escolhe posições aleatórias (não joga estrategicamente)")
    input("Pressione Enter para começar...")
    game_loop()