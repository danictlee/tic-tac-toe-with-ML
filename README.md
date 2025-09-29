# Projeto de IA - Classificador de Estados do Jogo da Velha

**Disciplina:** Inteligência Artificial  
**Instituição:** PUCRS - Pontifícia Universidade Católica do Rio Grande do Sul  
**Período:** 2025/02  
**Participantes** Daniel Lee, Gabriel Ottonelli, João Pedro Zarth, Lucas Brandt, Pedro Ernesto e Samuel Morales

---

## Visão Geral

Este projeto implementa um sistema completo de classificação de estados do jogo da velha utilizando diferentes algortimos de Machine Learning. O objetivo é classificar automaticamente o estado atual de uma partida em três categorias:

1. **"Fim de Jogo"** - A partida já terminou (vitória ou empate)
2. **"Possibilidade de Fim"** - Alguém pode ganhar na próxima jogada  
3. **"Tem Jogo"** - O jogo continua sem ameaça iminente

---

## Estrutura do Projeto


01_data_engineering.ipynb           # Carregamento e divisão do dataset, pré-processamento
02_training_and_evaluation.ipynb    # Treinamento e avaliação dos modelos
03_game_app.py                      # Aplicação do jogo interativo
dataset-IA.csv                      # Dataset original
train_dataset.csv                   # Dados de treino (gerado automaticamente)
validation_dataset.csv              # Dados de validação (gerado automaticamente)
test_dataset.csv                    # Dados de teste (gerado automaticamente)
best_classifier.joblib              # Melhor modelo treinado (gerado automaticamente)
onehot_encoder.joblib               # Encoder das posições (gerado automaticamente)
label_encoder.joblib                # Encoder das classes (gerado automaticamente)
comparacao_modelos.png              # Gráfico de comparação (gerado automaticamente)


## Como Executar

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
- `posicoes_encoder.joblib`
- `classes_encoder.joblib`
- `distribuicao_classes_carregado.png`

### Passo 2: Training and Evaluation
Execute o notebook `02_training_and_evaluation.ipynb` sequencialmente:

1. **Importações**: Carrega bibliotecas de ML
2. **Carregamento dos Dados**: Carrega datasets processados
3. **Otimização de Hiperparâmetros**: Treina 4 modelos diferentes
   - k-Nearest Neighbors (k-NN)
   - Decision Tree
   - Multi-layer Perceptron (MLP)
   - Random Forest
4. **Avaliação**: Compara modelos no conjunto de teste
5. **Visualização**: Gera gráfico comparativo
6. **Seleção**: Salva os modelos

**Arquivos gerados:**
- `dt_model.joblib`
- `knn_model.joblib`
- `mlp_model.joblib`
- `rf_model.joblib`
- `comparacao_modelos.png`

### Passo 3: Aplicação Interativa
Execute a aplicação web:

```bash
python web_app.py
```

Acesse pelo navegador em [http://localhost:5000](http://localhost:5000).

<!--
Se desejar testar via terminal:

```bash
python 03_game_app.py
```
-->