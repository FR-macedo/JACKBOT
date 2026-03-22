

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, r2_score
from sklearn.preprocessing import LabelEncoder

# --- Configuration ---
CHARTS_DIR = 'charts'

def visualize_team_outcome_model():
    """
    Trains the improved classification model (XGBoost) and generates a confusion matrix chart.
    """
    print("--- Visualizing Improved Model 1: Match Outcome (XGBoost) ---")
    
    if not os.path.exists(CHARTS_DIR):
        os.makedirs(CHARTS_DIR)
        
    try:
        df = pd.read_csv('wc2022_team_outcome.csv')
    except FileNotFoundError:
        print("Error: wc2022_team_outcome.csv not found. Please run data_processing.py first.")
        return

    features = [col for col in df.columns if 'ht_' in col or '_diff' in col]
    target = 'final_outcome'
    
    X = df[features].fillna(0)
    y = df[target]

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)
    
    # Re-using the same GridSearch logic from the training script for consistency
    param_grid = {
        'n_estimators': [100, 200], 'max_depth': [3, 5, 7], 'learning_rate': [0.05, 0.1],
        'subsample': [0.8, 1.0], 'colsample_bytree': [0.8, 1.0]
    }
    xgb_clf = xgb.XGBClassifier(objective='multi:softprob', eval_metric='mlogloss', use_label_encoder=False, random_state=42)
    grid_search = GridSearchCV(estimator=xgb_clf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=0, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    
    # Generate Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', xticklabels=le.classes_, yticklabels=le.classes_)
    plt.title('Matriz de Confusão - Previsão de Resultado da Partida (Aprimorado)')
    plt.xlabel('Previsto')
    plt.ylabel('Real')
    
    chart_path = os.path.join(CHARTS_DIR, 'improved_outcome_confusion_matrix.png')
    plt.savefig(chart_path)
    print(f"Gráfico da matriz de confusão salvo em: {chart_path}")
    plt.close()
    # Return results for the final report
    return y_test, y_pred, le.classes_

def create_regression_scatter_plot(model_name, y_test, y_pred, r2, file_name):
    """Helper function to create and save a scatter plot for regression models."""
    plt.figure(figsize=(8, 8))
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.6, color='green')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--', color='red', lw=2)
    plt.title(f'{model_name} (Aprimorado)\nPredito vs. Real (R² = {r2:.2f})')
    plt.xlabel('Valores Reais')
    plt.ylabel('Valores Previstos')
    plt.grid(True)
    
    chart_path = os.path.join(CHARTS_DIR, file_name)
    plt.savefig(chart_path)
    print(f"Gráfico de dispersão salvo em: {chart_path}")
    plt.close()

def visualize_team_sog_model():
    """
    Trains the improved regression model and generates a scatter plot.
    """
    print("\n--- Visualizing Improved Model 2: Team SOG Prediction (XGBoost) ---")

    try:
        df_team = pd.read_csv('wc2022_team_sog.csv')
        X_team = df_team[[col for col in df_team.columns if 'ht_' in col]].fillna(0)
        y_team = df_team['total_shots_on_goal']
        X_train_t, X_test_t, y_train_t, y_test_t = train_test_split(X_team, y_team, test_size=0.2, random_state=42)
        
        model_team = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
        model_team.fit(X_train_t, y_train_t)
        y_pred_t = model_team.predict(X_test_t)
        r2_team = r2_score(y_test_t, y_pred_t)
        
        create_regression_scatter_plot(
            'Previsão de Chutes a Gol do Time', 
            y_test_t, y_pred_t, r2_team, 
            'improved_team_sog_scatter.png'
        )
        return y_test_t, y_pred_t
    except FileNotFoundError:
        print("Error: wc2022_team_sog.csv not found.")
        return None, None

def main():
    """
    Main function to run all improved model visualizations.
    """
    # We don't need the results for the report here, but this structure allows for it
    visualize_team_outcome_model()
    visualize_team_sog_model()

if __name__ == '__main__':
    main()
