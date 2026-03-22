import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import confusion_matrix, r2_score
from sklearn.preprocessing import LabelEncoder

# --- Configuration ---
CHARTS_DIR = 'charts'

def visualize_team_outcome_model():
    """
    Trains the baseline classification model and generates a confusion matrix chart.
    """
    print("--- Visualizing Baseline Model 1: Match Outcome ---")
    
    if not os.path.exists(CHARTS_DIR):
        os.makedirs(CHARTS_DIR)
        
    try:
        df = pd.read_csv('wc2022_team_outcome.csv')
    except FileNotFoundError:
        print("Error: wc2022_team_outcome.csv not found. Please run data_processing.py first.")
        return

    features = [col for col in df.columns if 'ht_' in col and '_diff' not in col]
    target = 'final_outcome'
    
    X = df[features].fillna(0)
    y = df[target]

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)
    
    model = RandomForestClassifier(random_state=42, n_estimators=100)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    # Generate Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=le.classes_, yticklabels=le.classes_)
    plt.title('Matriz de Confusão - Previsão de Resultado da Partida (Baseline)')
    plt.xlabel('Previsto')
    plt.ylabel('Real')
    
    chart_path = os.path.join(CHARTS_DIR, 'baseline_outcome_confusion_matrix.png')
    plt.savefig(chart_path)
    print(f"Gráfico da matriz de confusão salvo em: {chart_path}")
    plt.close()

def create_regression_scatter_plot(model_name, y_test, y_pred, r2, file_name):
    """Helper function to create and save a scatter plot for regression models."""
    plt.figure(figsize=(8, 8))
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.6)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--', color='red', lw=2)
    plt.title(f'{model_name} (Baseline)\nPredito vs. Real (R² = {r2:.2f})')
    plt.xlabel('Valores Reais')
    plt.ylabel('Valores Previstos')
    plt.grid(True)
    
    chart_path = os.path.join(CHARTS_DIR, file_name)
    plt.savefig(chart_path)
    print(f"Gráfico de dispersão salvo em: {chart_path}")
    plt.close()

def visualize_regression_models():
    """
    Trains baseline regression models and generates scatter plots for their predictions.
    """
    print("\n--- Visualizing Baseline Models 2 & 3: SOG Predictions ---")

    # Team SOG Model
    try:
        df_team = pd.read_csv('wc2022_team_sog.csv')
        X_team = df_team[[col for col in df_team.columns if 'ht_' in col]].fillna(0)
        y_team = df_team['total_shots_on_goal']
        X_train_t, X_test_t, y_train_t, y_test_t = train_test_split(X_team, y_team, test_size=0.2, random_state=42)
        
        model_team = RandomForestRegressor(random_state=42, n_estimators=100)
        model_team.fit(X_train_t, y_train_t)
        y_pred_t = model_team.predict(X_test_t)
        r2_team = r2_score(y_test_t, y_pred_t)
        
        create_regression_scatter_plot(
            'Previsão de Chutes a Gol do Time', 
            y_test_t, y_pred_t, r2_team, 
            'baseline_team_sog_scatter.png'
        )
    except FileNotFoundError:
        print("Error: wc2022_team_sog.csv not found.")

    # Player SOG Model
    try:
        df_player = pd.read_csv('wc2022_player_sog.csv')
        X_player = df_player[[col for col in df_player.columns if 'ht_' in col]].fillna(0)
        y_player = df_player['total_shots_on_goal']
        X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(X_player, y_player, test_size=0.2, random_state=42)

        model_player = RandomForestRegressor(random_state=42, n_estimators=100)
        model_player.fit(X_train_p, y_train_p)
        y_pred_p = model_player.predict(X_test_p)
        r2_player = r2_score(y_test_p, y_pred_p)

        create_regression_scatter_plot(
            'Previsão de Chutes a Gol do Jogador', 
            y_test_p, y_pred_p, r2_player,
            'baseline_player_sog_scatter.png'
        )
    except FileNotFoundError:
        print("Error: wc2022_player_sog.csv not found.")

def main():
    """
    Main function to run all baseline model visualizations.
    """
    visualize_team_outcome_model()
    visualize_regression_models()

if __name__ == '__main__':
    main()
