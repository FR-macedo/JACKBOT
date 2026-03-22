# JACKBOT MVP Planning Document (Ultra-Lean Scope)

## 1. Goal of the MVP

The primary goal of this ultra-lean JACKBOT MVP is to rapidly demonstrate the core predictive power of our machine learning model for **Player Shots on Goal**. This MVP will be a standalone Python script with a Command-Line Interface (CLI), focusing on delivering a functional prediction within a 2-3 day timeframe.

## 2. Key Features

The MVP will include the following core functionality:

*   **Player Shots on Goal Prediction (CLI-based):**
    *   A Python script that loads a pre-trained model.
    *   Takes user input via the command line for a specific player and hypothetical match context (e.g., player name, competition type, half-time passes, touches, dribbles, and historical average performance metrics).
    *   Outputs a prediction for the total number of shots on goal for that player in the given match.
*   **No Web UI:** No graphical user interface will be developed for this MVP.
*   **No Language Model Integration:** The Language Model component is excluded from this scope.
*   **No Betting Functionality:** Simulated or real betting features are excluded.

## 3. Technology Stack

*   **Programming Language:** Python
*   **Data Manipulation:** Pandas
*   **Machine Learning:** Scikit-learn (`GradientBoostingRegressor`)
*   **Data Storage:** CSV files (for processed data and model persistence)
*   **Model Persistence:** Joblib or Pickle (to save and load the trained model).
*   **User Interface:** Command-Line Interface (CLI).
*   **Version Control:** Git (managed by user)

## 4. Data Requirements

The MVP will utilize the existing processed datasets:

*   `combined_player_sog.csv` (for training the model).

## 5. Model Selection

*   **Player Shots on Goal:** `GradientBoostingRegressor` (as it showed the best performance so far). The model will be trained once and saved.

## 6. User Interface (CLI)

A simple Python script that prompts the user for input and displays the prediction directly in the terminal.

## 7. Deployment Strategy (Basic)

The MVP will be a single, runnable Python script that operates locally on a user's machine.

## 8. Success Metrics

*   **Functionality:** The CLI script successfully loads the model, takes input, and provides a prediction without errors.
*   **Model Performance:** The underlying `GradientBoostingRegressor` achieves an R2 score of at least 0.26 (current best) and MAE of 0.24 (current best) on its test set.
*   **Timeliness:** MVP is delivered within 2-3 days.

## 9. Future Enhancements (Beyond MVP)

*   Expansion to Team Shots on Goal and Match Outcome predictions.
*   Development of a web-based user interface.
*   Integration of a Local Language Model for personalized recommendations.
*   Real-time data acquisition and prediction.
*   Incorporation of advanced features (xG, xA, player roles, tactical data).
*   Scalable cloud deployment.
*   Advanced user profiling and adaptive recommendations.
*   Explainable AI (XAI) for model predictions.
*   Expansion to other sports.