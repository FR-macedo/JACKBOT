import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define paths to the datasets
BASE_DIR = 'C:/Users/maced/Documents/Projetos/JACKBOT'
TEAM_OUTCOME_PATH = os.path.join(BASE_DIR, 'wc2022_team_outcome.csv')
TEAM_SOG_PATH = os.path.join(BASE_DIR, 'wc2022_team_sog.csv')
PLAYER_SOG_PATH = os.path.join(BASE_DIR, 'wc2022_player_sog.csv')

def load_and_display_info(file_path, name):
    """Loads a CSV, displays its head, info, and descriptive statistics."""
    print(f"\n--- {name} Data ---")
    df = pd.read_csv(file_path)
    print("Head:")
    print(df.head())
    print("\nInfo:")
    df.info()
    print("\nDescriptive Statistics:")
    print(df.describe())
    return df

def analyze_team_outcome(df):
    """Performs specific analysis for the team outcome dataset."""
    print("\n--- Team Outcome Analysis ---")
    
    # Distribution of final outcomes
    plt.figure(figsize=(8, 6))
    sns.countplot(x='final_outcome', data=df, palette='viridis')
    plt.title('Distribution of Match Outcomes')
    plt.xlabel('Match Outcome')
    plt.ylabel('Number of Matches')
    plt.show()

    # Correlation matrix for numerical features
    plt.figure(figsize=(12, 10))
    sns.heatmap(df.drop(['match_id', 'home_team_id', 'away_team_id'], axis=1).corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix for Team Outcome Features')
    plt.show()

    # Example: Half-time goals difference vs. final outcome
    plt.figure(figsize=(10, 7))
    sns.boxplot(x='final_outcome', y='ht_goals_diff', data=df, palette='plasma')
    plt.title('Half-time Goal Difference by Final Outcome')
    plt.xlabel('Final Outcome')
    plt.ylabel('Half-time Goal Difference (Home - Away)')
    plt.show()

def analyze_team_sog(df):
    """Performs specific analysis for the team shots on goal dataset."""
    print("\n--- Team Shots on Goal Analysis ---")

    # Distribution of total shots on goal
    plt.figure(figsize=(10, 6))
    sns.histplot(df['total_shots_on_goal'], bins=15, kde=True, palette='magma')
    plt.title('Distribution of Total Shots on Goal per Team')
    plt.xlabel('Total Shots on Goal')
    plt.ylabel('Frequency')
    plt.show()

    # Correlation with half-time stats
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.drop(['match_id', 'team_id'], axis=1).corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix for Team SOG Features')
    plt.show()

def analyze_player_sog(df):
    """Performs specific analysis for the player shots on goal dataset."""
    print("\n--- Player Shots on Goal Analysis ---")

    # Top players by total shots on goal
    top_players = df.groupby('player_name')['total_shots_on_goal'].sum().nlargest(10).sort_values(ascending=False)
    plt.figure(figsize=(12, 7))
    sns.barplot(x=top_players.values, y=top_players.index, palette='rocket')
    plt.title('Top 10 Players by Total Shots on Goal')
    plt.xlabel('Total Shots on Goal')
    plt.ylabel('Player Name')
    plt.show()

    # Correlation with half-time player stats
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.drop(['match_id', 'player_id', 'team_id'], axis=1).corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix for Player SOG Features')
    plt.show()


def main():
    """Main function to run the EDA."""
    df_team_outcome = load_and_display_info(TEAM_OUTCOME_PATH, "Team Outcome")
    df_team_sog = load_and_display_info(TEAM_SOG_PATH, "Team Shots on Goal")
    df_player_sog = load_and_display_info(PLAYER_SOG_PATH, "Player Shots on Goal")

    analyze_team_outcome(df_team_outcome)
    analyze_team_sog(df_team_sog)
    analyze_player_sog(df_player_sog)

if __name__ == '__main__':
    main()
