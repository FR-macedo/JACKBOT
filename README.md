# JACKBOT: A Sports Analytics & Prediction Project

This repository contains the source code and research for **JACKBOT**, a project focused on applying machine learning techniques to predict outcomes in soccer matches. This is a research-oriented project aimed at exploring the viability of different predictive models.

## Project Goal

The primary objective is to build and evaluate models that can predict various events within a soccer match, using event data from the first half to forecast final results. The main prediction tasks are:

1.  **Match Outcome Prediction (Classification):** Predict whether the home team will Win, Lose, or Draw.
2.  **Team Shots on Goal (Regression):** Predict the total number of shots on goal for each team.
3.  **Player Shots on Goal (Regression):** Predict the total number of shots on goal for each individual player.

The initial scope is focused on the **FIFA World Cup 2022** dataset provided by StatsBomb.

## Current Status

Based on the initial model evaluation (`docs/initial_model_evaluation_report.md`):

*   ✅ **Match Outcome Model:** Highly promising, with an initial accuracy of **75%**.
*   ⚠️ **Team Shots on Goal Model:** Partially viable, explaining about **25%** of the variance (R² = 0.25). Further feature engineering is needed.
*   ❌ **Player Shots on Goal Model:** Not viable with the current features (R² < 0). This task has been deprioritized.

## Tech Stack

*   **Language:** Python
*   **Libraries:**
    *   Pandas
    *   Scikit-learn

## Setup and Usage

### 1. Prerequisites

*   Python 3.x
*   The StatsBomb open data for the FIFA World Cup 2022. You can find this dataset online. Place the `data` folder (containing `competitions.json`, `events/`, `matches/`, etc.) inside a `Datasets/` directory in the root of this project.
    *Note: The `.gitignore` file is configured to ignore the `Datasets/` directory.*

### 2. Installation

Clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd JACKBOT
pip install -r requirements.txt
```

### 3. Running the Scripts

1.  **Process the Raw Data:**
    Run the `data_processing.py` script to generate the structured CSV files from the raw JSON data.

    ```bash
    python data_processing.py
    ```
    This will create the following files in the root directory:
    *   `wc2022_team_outcome.csv`
    *   `wc2022_team_sog.csv`
    *   `wc2022_player_sog.csv`

2.  **Train and Evaluate the Models:**
    Run the `train_models.py` script to train the models and see their performance evaluation printed to the console.

    ```bash
    python train_models.py
    ```

## License

This project is currently not licensed. Please add a license file if you intend to share it publicly.
