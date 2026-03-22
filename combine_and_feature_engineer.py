import pandas as pd
import os

# Define paths to the datasets
BASE_DIR = 'C:/Users/maced/Documents/Projetos/JACKBOT'
WC_PLAYER_SOG_PATH = os.path.join(BASE_DIR, 'wc2022_player_sog.csv')
LIGUE1_PLAYER_SOG_PATH = os.path.join(BASE_DIR, 'ligue1_2021_2022_player_sog.csv')

def create_enriched_player_dataset():
    """
    Combines player SOG data from WC 2022 and Ligue 1 2021/2022,
    and adds cross-competition features.
    """
    df_wc = pd.read_csv(WC_PLAYER_SOG_PATH)
    df_ligue1 = pd.read_csv(LIGUE1_PLAYER_SOG_PATH)

    # Add competition type
    df_wc['competition_type'] = 'World Cup'
    df_ligue1['competition_type'] = 'Ligue 1'

    # Combine datasets
    combined_df = pd.concat([df_ligue1, df_wc], ignore_index=True)

    # One-hot encode competition_type
    combined_df = pd.get_dummies(combined_df, columns=['competition_type'], prefix='competition_type')

    # Calculate historical performance features from Ligue 1 for players
    # This assumes Ligue 1 is the "previous" competition for World Cup players
    # For players who only played in WC, these features will be NaN initially
    
    # Group Ligue 1 data by player to get average performance
    ligue1_avg_performance = df_ligue1.groupby('player_id').agg(
        avg_ht_passes_ligue1=('ht_passes', 'mean'),
        avg_ht_touches_ligue1=('ht_touches', 'mean'),
        avg_ht_dribbles_ligue1=('ht_dribbles', 'mean'),
        avg_total_sog_ligue1=('total_shots_on_goal', 'mean')
    ).reset_index()

    # Merge these historical features into the combined dataset
    # We'll merge based on player_id
    combined_df = pd.merge(
        combined_df,
        ligue1_avg_performance,
        on='player_id',
        how='left'
    )

    # Fill NaN values for players who didn't play in Ligue 1 (or for Ligue 1 entries themselves)
    # For Ligue 1 entries, their own Ligue 1 average is their "historical" performance
    # For WC players not in Ligue 1, these will remain NaN, which might need further handling (e.g., imputation)
    
    # For simplicity, let's fill NaN for Ligue 1 entries with their own match stats
    # This is a simplification and might need more sophisticated logic depending on the model's needs
    combined_df['avg_ht_passes_ligue1'] = combined_df.apply(
        lambda row: row['ht_passes'] if pd.isna(row['avg_ht_passes_ligue1']) and row['competition_type_Ligue 1'] == 1 else row['avg_ht_passes_ligue1'],
        axis=1
    )
    combined_df['avg_ht_touches_ligue1'] = combined_df.apply(
        lambda row: row['ht_touches'] if pd.isna(row['avg_ht_touches_ligue1']) and row['competition_type_Ligue 1'] == 1 else row['avg_ht_touches_ligue1'],
        axis=1
    )
    combined_df['avg_ht_dribbles_ligue1'] = combined_df.apply(
        lambda row: row['ht_dribbles'] if pd.isna(row['avg_ht_dribbles_ligue1']) and row['competition_type_Ligue 1'] == 1 else row['avg_ht_dribbles_ligue1'],
        axis=1
    )
    combined_df['avg_total_sog_ligue1'] = combined_df.apply(
        lambda row: row['total_shots_on_goal'] if pd.isna(row['avg_total_sog_ligue1']) and row['competition_type_Ligue 1'] == 1 else row['avg_total_sog_ligue1'],
        axis=1
    )

    # Create interaction features between player_id and one-hot encoded competition types
    combined_df['player_id_x_world_cup'] = combined_df['player_id'] * combined_df['competition_type_World Cup']
    combined_df['player_id_x_ligue_1'] = combined_df['player_id'] * combined_df['competition_type_Ligue 1']

    # Display info about the combined dataset
    print("\n--- Combined Player Dataset Info ---")
    print(combined_df.info())
    print("\n--- Combined Player Dataset Head ---")
    print(combined_df.head())
    print("\n--- Combined Player Dataset Tail ---")
    print(combined_df.tail())

    # Save the combined dataset
    combined_player_sog_path = os.path.join(BASE_DIR, 'combined_player_sog.csv')
    combined_df.to_csv(combined_player_sog_path, index=False)
    print(f"\nSuccessfully saved combined player SOG data to {combined_player_sog_path}")
    
    return combined_df

if __name__ == '__main__':
    create_enriched_player_dataset()
