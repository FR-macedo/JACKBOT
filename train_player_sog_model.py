import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import joblib
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder

# Define paths to the datasets
BASE_DIR = 'C:/Users/maced/Documents/Projetos/JACKBOT'
COMBINED_PLAYER_SOG_PATH = os.path.join(BASE_DIR, 'combined_player_sog.csv')

def train_and_evaluate_player_sog_model():
    """
    Loads the combined player SOG data, prepares it for modeling,
    trains a regression model, and evaluates its performance.
    """
    df = pd.read_csv(COMBINED_PLAYER_SOG_PATH)

    # --- Data Preparation ---
    
    # Handle NaN values in historical average features (simplistic imputation for now)
    # Fill with 0, assuming no prior performance if NaN
    historical_avg_cols = [col for col in df.columns if col.startswith('avg_')]
    for col in historical_avg_cols:
        df[col] = df[col].fillna(0)

    # Encode categorical features
    le_player = LabelEncoder()
    df['player_id_encoded'] = le_player.fit_transform(df['player_id'])
    
    le_team = LabelEncoder()
    df['team_id_encoded'] = le_team.fit_transform(df['team_id'])

    # Define features (X) and target (y)
    features = [
        'ht_passes', 'ht_touches', 'ht_dribbles',
        'competition_type_Ligue 1', 'competition_type_World Cup',
        'player_id_encoded', 'team_id_encoded',
        'player_id_x_world_cup', 'player_id_x_ligue_1'
    ] + historical_avg_cols # Include historical average features

    target = 'total_shots_on_goal'

    X = df[features]
    y = df[target]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"\n--- Model Training ---")
    print(f"Training data shape: {X_train.shape}")
    print(f"Testing data shape: {X_test.shape}")

    # --- Model Training ---
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)

    # --- Model Evaluation ---
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\n--- Model Evaluation ---")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"R-squared (R2): {r2:.2f}")

    # Feature Importance
    feature_importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
    print("\n--- Feature Importances ---")
    print(feature_importances)

    # Save the trained model and encoders
    model_output_dir = os.path.join(BASE_DIR, 'models')
    os.makedirs(model_output_dir, exist_ok=True)
    
    joblib.dump(model, os.path.join(model_output_dir, 'player_sog_model.joblib'))
    joblib.dump(le_player, os.path.join(model_output_dir, 'le_player.joblib'))
    joblib.dump(le_team, os.path.join(model_output_dir, 'le_team.joblib'))
    joblib.dump(features, os.path.join(model_output_dir, 'model_features.joblib'))
    
    print(f"\nModel and encoders saved to {model_output_dir}")

    return model, mae, r2, feature_importances

if __name__ == '__main__':
    train_and_evaluate_player_sog_model()
