# 🎯 AI Project - Tic-Tac-Toe Game State Classifier

This project implements a complete Machine Learning system to classify tic-tac-toe game states and an interactive application to test the model.

## 📁 Project Structure

```
📦 AI Project
├── 01_data_engineering.ipynb      # Data engineering pipeline
├── 02_training_and_evaluation.ipynb  # Model training and evaluation
├── 03_game_app.py                 # Interactive game application
├── dataset-IA.csv                 # Original dataset
├── train_dataset.csv              # Training data (auto-generated)
├── validation_dataset.csv         # Validation data (auto-generated)
├── test_dataset.csv               # Test data (auto-generated)
├── best_classifier.joblib         # Best trained model (auto-generated)
├── onehot_encoder.joblib           # Feature encoder (auto-generated)
├── label_encoder.joblib            # Class encoder (auto-generated)
└── model_comparison.png            # Comparison chart (auto-generated)
```

## 🚀 How to Run

### Prerequisites
- Python 3.8+
- Jupyter Notebook or VS Code with Python extension
- Libraries: pandas, numpy, scikit-learn, matplotlib, seaborn, joblib

### Step 1: Data Engineering
Run the notebook `01_data_engineering.ipynb` sequentially:

1. **Setup and Imports**: Installs dependencies and imports libraries
2. **Data Loading**: Loads and analyzes the dataset
3. **Exploratory Analysis**: Checks class balance
4. **Preprocessing**: Encodes features and splits data

**Generated files:**
- `train_dataset.csv`
- `validation_dataset.csv`  
- `test_dataset.csv`
- `onehot_encoder.joblib`
- `label_encoder.joblib`
- `class_distribution_loaded.png`

### Step 2: Training and Evaluation
Run the notebook `02_training_and_evaluation.ipynb` sequentially:

1. **Imports**: Loads ML libraries
2. **Data Loading**: Loads processed datasets
3. **Hyperparameter Optimization**: Trains 5 different models
   - k-Nearest Neighbors (k-NN)
   - Decision Tree
   - Multi-layer Perceptron (MLP)
   - Random Forest
   - Support Vector Machine (SVM)
4. **Evaluation**: Compares models on test set
5. **Visualization**: Generates comparison chart
6. **Selection**: Saves the best model

**Generated files:**
- `best_classifier.joblib`
- `model_comparison.png`

### Step 3: Interactive Application
Run the game in terminal:

```bash
python 03_game_app.py
```

## 🎮 How to Play

1. The tic-tac-toe board will be displayed with positions numbered 1-9
2. You play as 'X' and the computer as 'O'
3. Enter the position number where you want to play
4. The AI will analyze each game state and show:
   - Real game state
   - AI prediction
   - Whether the prediction is correct
   - Real-time accuracy

## 📊 Dataset Classes

- **Game Over**: Game finished (victory or draw)
- **Possibility of End**: Someone can win in the next move
- **Has Game**: Game still in progress without immediate threats

## 🧠 Implemented Models

1. **k-NN**: Classification based on nearest neighbors
2. **Decision Tree**: Decision tree with optimized criteria
3. **MLP**: Multi-layer neural network
4. **Random Forest**: Ensemble of decision trees
5. **SVM**: Support vector machine

## 📈 Evaluation Metrics

- **Weighted F1-Score**: Main metric for best model selection
- **Classification Report**: Precision, Recall and F1-Score per class
- **Real-time Accuracy**: During interactive gameplay

## 🔧 Features

### Data Pipeline
- ✅ Automatic dataset loading and validation
- ✅ Exploratory analysis with visualizations
- ✅ Categorical variable encoding (One-Hot)
- ✅ Stratified data split (80% train, 10% validation, 10% test)

### Model Training
- ✅ Grid Search for hyperparameter optimization
- ✅ 5-fold cross-validation
- ✅ Automatic model comparison
- ✅ Best model saving

### Interactive Application
- ✅ Intuitive terminal interface
- ✅ Real-time game state analysis
- ✅ AI accuracy calculation during gameplay
- ✅ Automatic game end detection

## 🎯 Project Objective

This project demonstrates a complete Machine Learning pipeline:
1. **Data Engineering**: Data preparation and analysis
2. **Modeling**: Training and comparison of multiple algorithms
3. **Practical Application**: Interactive system for model validation

The result is an AI capable of classifying tic-tac-toe game states with high precision, useful for automated game systems or strategic analysis.

---
*Developed as an educational Machine Learning project*