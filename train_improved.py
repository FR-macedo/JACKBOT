import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder

# --- Baseline Scores from Iteration 1 ---
BASELINE_ACCURACY = 0.75
BASELINE_R2_TEAM = 0.25
BASELINE_R2_PLAYER = -0.02

def train_team_outcome_model():
    """
    Trains and evaluates an XGBoost classification model to predict match outcomes.
    Includes hyperparameter tuning.
    """
    print("--- Iteration 2 - Model 1: Predicting Match Outcome (XGBoost) ---")
    
    # Load data
    try:
        df = pd.read_csv('wc2022_team_outcome.csv')
    except FileNotFoundError:
        print("Error: wc2022_team_outcome.csv not found. Please run data_processing.py first.")
        return

    # Define features (X) and target (y) - now including difference features
    features = [col for col in df.columns if 'ht_' in col or '_diff' in col]
    target = 'final_outcome'
    
    X = df[features]
    y = df[target]
    
    X = X.fillna(0)

    # Encode target labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)
    
    # --- XGBoost with Hyperparameter Tuning ---
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.05, 0.1],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0]
    }
    
    xgb_clf = xgb.XGBClassifier(objective='multi:softprob', eval_metric='mlogloss', use_label_encoder=False, random_state=42)
    
    # Using GridSearchCV to find the best parameters
    grid_search = GridSearchCV(estimator=xgb_clf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=1, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    
    print(f"Best parameters found: {grid_search.best_params_}")
    
    # Evaluate model with best parameters
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=le.classes_, zero_division=0)
    
    print(f"\nBaseline Accuracy (RandomForest): {BASELINE_ACCURACY:.2f}")
    print(f"New Model Accuracy (XGBoost): {accuracy:.2f}")
    print(f"Improvement: {accuracy - BASELINE_ACCURACY:+.2f}")
    print("\nClassification Report:")
    print(report)
    print("-" * 60)

def train_team_sog_model():
    """
    Trains and evaluates an XGBoost regression model to predict team shots on goal.
    """
    print("--- Iteration 2 - Model 2: Predicting Team Shots on Goal (XGBoost) ---")
    
    # Load data
    try:
        df = pd.read_csv('wc2022_team_sog.csv')
    except FileNotFoundError:
        print("Error: wc2022_team_sog.csv not found. Please run data_processing.py first.")
        return

    # Define features (X) and target (y)
    features = [col for col in df.columns if 'ht_' in col]
    target = 'total_shots_on_goal'
    
    X = df[features]
    y = df[target]

    X = X.fillna(0)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model (using default XGBoost parameters for simplicity, tuning can be added)
    model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nMean Absolute Error (MAE): {mae:.2f}")
    print(f"Baseline R-squared (RandomForest): {BASELINE_R2_TEAM:.2f}")
    print(f"New Model R-squared (XGBoost): {r2:.2f}")
    print(f"Improvement: {r2 - BASELINE_R2_TEAM:+.2f}")
    print(f"(The new model explains {r2:.2%} of the variance in team shots on goal.)")
    print("-" * 60)

def train_player_sog_model():
    """
    Confirms the previous finding that this model is not viable with current features.
    """
    print("--- Iteration 2 - Model 3: Predicting Player Shots on Goal (Confirmation) ---")
    print("This model was found to be inviable in the first iteration (R² < 0).")
    print("The simple features available are not predictive for this complex task.")
    print("Skipping retraining as per the iteration plan. This task is deprioritized.")
    print(f"Baseline R-squared (RandomForest): {BASELINE_R2_PLAYER:.2f}")
    print("-" * 60)


def main():
    """
    Main function to run all model training and evaluation for Iteration 2.
    """
    train_team_outcome_model()
    train_team_sog_model()
    train_player_sog_model()

if __name__ == '__main__':
    main()