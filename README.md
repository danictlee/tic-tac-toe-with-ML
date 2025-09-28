# 🎯 Projeto de IA - Classificador de Estados do Jogo da Velha

Este projeto implementa um sistema completo de Machine Learning para classificar estados do jogo da velha e uma aplicação interativa para testar o modelo.

## 📁 Estrutura do Projeto

```
📦 Projeto IA
├── 01_data_engineering.ipynb      # Pipeline de engenharia de dados
├── 02_training_and_evaluation.ipynb  # Treinamento e avaliação dos modelos
├── 03_game_app.py                 # Aplicação do jogo interativo
├── dataset-IA.csv                 # Dataset original
├── train_dataset.csv              # Dados de treino (gerado automaticamente)
├── validation_dataset.csv         # Dados de validação (gerado automaticamente)
├── test_dataset.csv               # Dados de teste (gerado automaticamente)
├── best_classifier.joblib         # Melhor modelo treinado (gerado automaticamente)
├── onehot_encoder.joblib           # Encoder das features (gerado automaticamente)
├── label_encoder.joblib            # Encoder das classes (gerado automaticamente)
└── comparacao_modelos.png          # Gráfico de comparação (gerado automaticamente)
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- Jupyter Notebook ou VS Code com extensão Python
- Bibliotecas: pandas, numpy, scikit-learn, matplotlib, seaborn, joblib

### Passo 1: Data Engineering
Execute o notebook `01_data_engineering.ipynb` sequencialmente:

1. **Setup e Importações**: Instala dependências e importa bibliotecas
2. **Carregamento dos Dados**: Carrega e analisa o dataset
3. **Análise Exploratória**: Verifica balanceamento das classes
4. **Pré-processamento**: Codifica features e divide os dados

**Arquivos gerados:**
- `train_dataset.csv`
- `validation_dataset.csv`  
- `test_dataset.csv`
- `onehot_encoder.joblib`
- `label_encoder.joblib`
- `distribuicao_classes_carregado.png`

### Passo 2: Training and Evaluation
Execute o notebook `02_training_and_evaluation.ipynb` sequencialmente:

1. **Importações**: Carrega bibliotecas de ML
2. **Carregamento dos Dados**: Carrega datasets processados
3. **Otimização de Hiperparâmetros**: Treina 5 modelos diferentes
   - k-Nearest Neighbors (k-NN)
   - Decision Tree
   - Multi-layer Perceptron (MLP)
   - Random Forest
   - Support Vector Machine (SVM)
4. **Avaliação**: Compara modelos no conjunto de teste
5. **Visualização**: Gera gráfico comparativo
6. **Seleção**: Salva o melhor modelo

**Arquivos gerados:**
- `best_classifier.joblib`
- `comparacao_modelos.png`

### Passo 3: Aplicação Interativa
Execute o jogo no terminal:

```bash
python 03_game_app.py
```

## 🎮 Como Jogar

1. O jogo da velha será exibido com posições numeradas de 1-9
2. Você joga como 'X' e o computador como 'O'
3. Digite o número da posição onde quer jogar
4. A IA analisará cada estado do jogo e mostrará:
   - Estado real do jogo
   - Predição da IA
   - Se a predição está correta
   - Acurácia em tempo real

## 📊 Classes do Dataset

- **Fim de Jogo**: Jogo terminado (vitória ou empate)
- **Possibilidade de Fim**: Alguém pode ganhar na próxima jogada
- **Tem Jogo**: Jogo ainda em andamento sem ameaças imediatas

## 🧠 Modelos Implementados

1. **k-NN**: Classificação baseada em vizinhos próximos
2. **Decision Tree**: Árvore de decisão com critérios otimizados
3. **MLP**: Rede neural multi-camadas
4. **Random Forest**: Ensemble de árvores de decisão
5. **SVM**: Máquina de vetores de suporte

## 📈 Métricas de Avaliação

- **F1-Score Ponderado**: Métrica principal para seleção do melhor modelo
- **Classification Report**: Precision, Recall e F1-Score por classe
- **Acurácia em Tempo Real**: Durante o jogo interativo

## 🔧 Funcionalidades

### Pipeline de Dados
- ✅ Carregamento e validação automática do dataset
- ✅ Análise exploratória com visualizações
- ✅ Codificação de variáveis categóricas (One-Hot)
- ✅ Divisão estratificada dos dados (80% treino, 10% validação, 10% teste)

### Treinamento de Modelos
- ✅ Grid Search para otimização de hiperparâmetros
- ✅ Validação cruzada 5-fold
- ✅ Comparação automática de modelos
- ✅ Salvamento do melhor modelo

### Aplicação Interativa
- ✅ Interface de terminal intuitiva
- ✅ Análise em tempo real dos estados do jogo
- ✅ Cálculo de acurácia da IA durante o jogo
- ✅ Detecção automática de fim de jogo

## 🎯 Objetivo do Projeto

Este projeto demonstra um pipeline completo de Machine Learning:
1. **Engenharia de Dados**: Preparação e análise dos dados
2. **Modelagem**: Treinamento e comparação de múltiplos algoritmos
3. **Aplicação Prática**: Sistema interativo para validação do modelo

O resultado é uma IA capaz de classificar estados do jogo da velha com alta precisão, útil para sistemas de jogos automatizados ou análise estratégica.

---
*Desenvolvido como projeto educacional de Machine Learning*