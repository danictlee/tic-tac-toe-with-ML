# 🎯 Projeto de IA - Classificador de Estados do Jogo da Velha

**Disciplina:** Inteligência Artificial  
**Instituição:** PUCRS - Pontifícia Universidade Católica do Rio Grande do Sul  
**Período:** 2025/02  

---

## 📚 Visão Geral

Este projeto implementa um **sistema completo de classificação de estados do jogo da velha** utilizando técnicas de **Machine Learning**. O objetivo é classificar automaticamente o estado atual de uma partida em três categorias:

1. **"Fim de Jogo"** - A partida já terminou (vitória ou empate)
2. **"Possibilidade de Fim"** - Alguém pode ganhar na próxima jogada  
3. **"Tem Jogo"** - O jogo continua sem ameaça iminente

---

## 🏗️ Arquitetura do Projeto

### Pipeline de Desenvolvimento:
```
Dataset Raw → Data Engineering → Model Training → Model Evaluation → Deployment
     ↓              ↓                 ↓               ↓               ↓
dataset-IA.csv → 01_notebook → 02_notebook → best_model.joblib → Web App
```

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

### Machine Learning
- ✅ Otimização de hiperparâmetros com GridSearchCV
- ✅ Validação cruzada k-fold (k=5)
- ✅ Comparação de 5 algoritmos diferentes
- ✅ Seleção automática do melhor modelo
- ✅ Avaliação com métricas robustas (F1-Score ponderado)

### Aplicações Interativas
- ✅ Jogo da velha no terminal com predições em tempo real
- ✅ Interface web moderna e responsiva
- ✅ Dashboard de análise da IA
- ✅ Histórico de predições e estatísticas
- ✅ API REST para integração

---

## 🎯 Resultados Esperados

- **Acurácia:** >90% na classificação de estados
- **F1-Score:** >0.90 ponderado entre todas as classes  
- **Tempo de Resposta:** <1ms por predição
- **Interface:** Responsiva e intuitiva para demonstrações

---

## 📋 Arquivos do Projeto

```
projeto/
├── 00_project_overview.ipynb      # Visão geral e documentação
├── 01_data_engineering.ipynb      # Pipeline de dados
├── 02_training_and_evaluation.ipynb # Treinamento de modelos
├── 03_game_app.py                 # Jogo terminal
├── web_app.py                     # Aplicação web Flask
├── dataset-IA.csv                 # Dataset original
├── README.md                      # Esta documentação
├── static/                        # Recursos frontend
│   ├── styles.css                 # Estilos CSS modernos
│   └── script.js                  # JavaScript interativo
└── templates/
    └── index.html                 # Template HTML responsivo
```

---

## 🔬 Aspectos Técnicos

- **Linguagem:** Python 3.8+
- **Framework ML:** Scikit-learn  
- **Framework Web:** Flask
- **Frontend:** HTML5, CSS3, JavaScript ES6+
- **Visualização:** Matplotlib, Seaborn
- **Persistência:** Joblib para modelos, CSV para dados
- **Responsividade:** Design mobile-first

---

## 👨‍💻 Autor

**Desenvolvido para a disciplina de Inteligência Artificial**  
PUCRS - Pontifícia Universidade Católica do Rio Grande do Sul  
Semestre: 2025/02

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