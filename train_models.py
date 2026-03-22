
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder

def train_team_outcome_model():
    """
    Trains and evaluates a classification model to predict match outcomes.
    """
    print("--- Model 1: Predicting Match Outcome (Win/Loss/Draw) ---")
    
    # Load data
    try:
        df = pd.read_csv('wc2022_team_outcome.csv')
    except FileNotFoundError:
        print("Error: wc2022_team_outcome.csv not found. Please run data_processing.py first.")
        return

    # Define features (X) and target (y)
    features = [col for col in df.columns if 'ht_' in col]
    target = 'final_outcome'
    
    X = df[features]
    y = df[target]
    
    # Handle potential missing values
    X = X.fillna(0)

    # Encode target labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.25, random_state=42, stratify=y_encoded)
    
    # Train model
    model = RandomForestClassifier(random_state=42, n_estimators=100)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=le.classes_, zero_division=0)
    
    print(f"Model Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(report)
    print("-" * 50)

def train_team_sog_model():
    """
    Trains and evaluates a regression model to predict team shots on goal.
    """
    print("--- Model 2: Predicting Team Shots on Goal ---")
    
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

    # Handle potential missing values
    X = X.fillna(0)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    # Train model
    model = RandomForestRegressor(random_state=42, n_estimators=100)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"(On average, the model's prediction is off by ~{mae:.2f} shots on goal.)")
    print(f"R-squared (R²): {r2:.2f}")
    print(f"(The model explains {r2:.2%} of the variance in team shots on goal.)")
    print("-" * 50)

def train_player_sog_model():
    """
    Trains and evaluates a regression model to predict player shots on goal.
    """
    print("--- Model 3: Predicting Player Shots on Goal ---")
    
    # Load data
    try:
        df = pd.read_csv('wc2022_player_sog.csv')
    except FileNotFoundError:
        print("Error: wc2022_player_sog.csv not found. Please run data_processing.py first.")
        return

    # Define features (X) and target (y)
    features = [col for col in df.columns if 'ht_' in col]
    target = 'total_shots_on_goal'
    
    X = df[features]
    y = df[target]

    # Handle potential missing values
    X = X.fillna(0)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    # Train model
    model = RandomForestRegressor(random_state=42, n_estimators=100)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"(On average, the model's prediction is off by ~{mae:.2f} shots on goal.)")
    print(f"R-squared (R²): {r2:.2f}")
    print(f"(The model explains {r2:.2%} of the variance in player shots on goal.)")
    print("-" * 50)

def main():
    """
    Main function to run all model training and evaluation.
    """
    train_team_outcome_model()
    train_team_sog_model()
    train_player_sog_model()

if __name__ == '__main__':
    main()
