import pandas as pd
import os

# Define paths to the datasets
BASE_DIR = 'C:/Users/maced/Documents/Projetos/JACKBOT'
WC_PLAYER_SOG_PATH = os.path.join(BASE_DIR, 'wc2022_player_sog.csv')
LIGUE1_PLAYER_SOG_PATH = os.path.join(BASE_DIR, 'ligue1_2021_2022_player_sog.csv')

def get_player_sog_data(file_path, player_name):
    """Loads player SOG data and filters for a specific player."""
    df = pd.read_csv(file_path)
    player_df = df[df['player_name'] == player_name]
    return player_df

def analyze_messi_performance():
    """Analyzes Messi's performance in WC 2022 and Ligue 1 2021/2022."""
    messi_wc_df = get_player_sog_data(WC_PLAYER_SOG_PATH, "Lionel Andrés Messi Cuccittini")
    messi_ligue1_df = get_player_sog_data(LIGUE1_PLAYER_SOG_PATH, "Lionel Andrés Messi Cuccittini")

    print("\n--- Lionel Messi - FIFA World Cup 2022 Performance (Shots on Goal) ---")
    if not messi_wc_df.empty:
        print(messi_wc_df.describe())
        print(f"\nTotal Shots on Goal in WC 2022: {messi_wc_df['total_shots_on_goal'].sum()}")
    else:
        print("Lionel Messi data not found in WC 2022 dataset.")

    print("\n--- Lionel Messi - Ligue 1 2021/2022 Performance (Shots on Goal) ---")
    if not messi_ligue1_df.empty:
        print(messi_ligue1_df.describe())
        print(f"\nTotal Shots on Goal in Ligue 1 2021/2022: {messi_ligue1_df['total_shots_on_goal'].sum()}")
    else:
        print("Lionel Messi data not found in Ligue 1 2021/2022 dataset.")

    # Further analysis and correlation can be added here
    # For example, comparing average shots on goal, or other metrics.
    if not messi_wc_df.empty and not messi_ligue1_df.empty:
        print("\n--- Comparative Analysis ---")
        wc_avg_sog = messi_wc_df['total_shots_on_goal'].mean()
        ligue1_avg_sog = messi_ligue1_df['total_shots_on_goal'].mean()
        
        print(f"Average Shots on Goal per match (WC 2022): {wc_avg_sog:.2f}")
        print(f"Average Shots on Goal per match (Ligue 1 2021/2022): {ligue1_avg_sog:.2f}")

        # Example of a simple correlation (though more complex analysis would be needed for true correlation)
        # Here we are just comparing the averages.
        if wc_avg_sog > ligue1_avg_sog:
            print("Messi had a higher average shots on goal per match in WC 2022 compared to Ligue 1 2021/2022.")
        elif ligue1_avg_sog > wc_avg_sog:
            print("Messi had a higher average shots on goal per match in Ligue 1 2021/2022 compared to WC 2022.")
        else:
            print("Messi had a similar average shots on goal per match in both competitions.")


if __name__ == '__main__':
    analyze_messi_performance()
