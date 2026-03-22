import json
import pandas as pd
import os
from tqdm import tqdm

# --- Configuration ---
BASE_DIR = 'C:/Users/maced/Documents/Projetos/JACKBOT/Datasets/data'
COMPETITIONS_FILE = os.path.join(BASE_DIR, 'competitions.json')
MATCH_DIR = os.path.join(BASE_DIR, 'matches')
EVENT_DIR = os.path.join(BASE_DIR, 'events')
LINEUP_DIR = os.path.join(BASE_DIR, 'lineups')

# --- Main Functions ---

def get_match_data_for_competition_season(target_competition_name, target_season_name):
    """
    Finds the competition_id and season_id for a given competition and season
    and returns all associated match_ids and match info.
    """
    with open(COMPETITIONS_FILE, 'r', encoding='utf-8') as f:
        competitions = json.load(f)

    comp_id, season_id = None, None
    for comp in competitions:
        if comp['competition_name'] == target_competition_name and comp['season_name'] == target_season_name:
            comp_id = comp['competition_id']
            season_id = comp['season_id']
            break

    if not comp_id:
        raise ValueError(f"{target_competition_name} {target_season_name} not found in competitions.json")

    matches_file = os.path.join(MATCH_DIR, str(comp_id), f'{season_id}.json')
    with open(matches_file, 'r', encoding='utf-8') as f:
        matches = json.load(f)

    match_ids = [match['match_id'] for match in matches]
    match_info = {match['match_id']: match for match in matches}
    
    print(f"Found {len(match_ids)} matches for {target_competition_name} {target_season_name}.")
    return match_ids, match_info

def process_data(match_ids, match_info):
    """
    Processes all matches to extract features and targets for three separate datasets.
    """
    # Lists to hold dictionaries, which will be converted to DataFrames
    team_outcome_data = []
    team_sog_data = []
    player_sog_data = []

    for match_id in tqdm(match_ids, desc="Processing Matches"):
        event_file = os.path.join(EVENT_DIR, f'{match_id}.json')
        lineup_file = os.path.join(LINEUP_DIR, f'{match_id}.json')

        with open(event_file, 'r', encoding='utf-8') as f:
            events = json.load(f)
        with open(lineup_file, 'r', encoding='utf-8') as f:
            lineups = json.load(f)
            
        match_details = match_info[match_id]
        home_team_id = match_details['home_team']['home_team_id']
        away_team_id = match_details['away_team']['away_team_id']
        
        # --- Feature Engineering ---
        
        # Convert events to DataFrame for easier manipulation
        events_df = pd.json_normalize(events, sep='_')
        
        # 1. Calculate full-match stats (for targets)
        sog_conditions = (events_df['shot_outcome_name'] == 'Goal') | (events_df['shot_outcome_name'] == 'Saved')
        full_match_sog = events_df[events_df['type_name'] == 'Shot'][sog_conditions]
        
        team_sog_total = full_match_sog.groupby('team_id').size().to_dict()
        player_sog_total = full_match_sog.groupby('player_id').size().to_dict()

        # 2. Calculate half-time features (for predictors)
        ht_events_df = events_df[events_df['period'] == 1].copy()
        
        ht_shots = ht_events_df[ht_events_df['type_name'] == 'Shot'].groupby('team_id').size().to_dict()
        ht_sog = ht_events_df[ht_events_df['type_name'] == 'Shot'][sog_conditions].groupby('team_id').size().to_dict()
        ht_corners = ht_events_df[ht_events_df['type_name'] == 'Corner'].groupby('team_id').size().to_dict()
        ht_fouls = ht_events_df[ht_events_df['type_name'] == 'Foul Committed'].groupby('team_id').size().to_dict()
        ht_goals = ht_events_df[ht_events_df['type_name'] == 'Shot'][ht_events_df['shot_outcome_name'] == 'Goal'].groupby('team_id').size().to_dict()

        # --- Assemble Datasets ---

        # Dataset 1: Team Outcome
        outcome = 'Draw'
        if match_details['home_score'] > match_details['away_score']:
            outcome = 'Win'
        elif match_details['home_score'] < match_details['away_score']:
            outcome = 'Loss'
        
        home_ht_goals = ht_goals.get(home_team_id, 0)
        away_ht_goals = ht_goals.get(away_team_id, 0)
        home_ht_shots = ht_shots.get(home_team_id, 0)
        away_ht_shots = ht_shots.get(away_team_id, 0)
        home_ht_sog = ht_sog.get(home_team_id, 0)
        away_ht_sog = ht_sog.get(away_team_id, 0)
        home_ht_corners = ht_corners.get(home_team_id, 0)
        away_ht_corners = ht_corners.get(away_team_id, 0)
        home_ht_fouls = ht_fouls.get(home_team_id, 0)
        away_ht_fouls = ht_fouls.get(away_team_id, 0)
            
        team_outcome_data.append({
            'match_id': match_id,
            'home_team_id': home_team_id,
            'away_team_id': away_team_id,
            'home_ht_goals': home_ht_goals,
            'away_ht_goals': away_ht_goals,
            'home_ht_shots': home_ht_shots,
            'away_ht_shots': away_ht_shots,
            'home_ht_sog': home_ht_sog,
            'away_ht_sog': away_ht_sog,
            'home_ht_corners': home_ht_corners,
            'away_ht_corners': away_ht_corners,
            'home_ht_fouls': home_ht_fouls,
            'away_ht_fouls': away_ht_fouls,
            # New Difference Features
            'ht_goals_diff': home_ht_goals - away_ht_goals,
            'ht_shots_diff': home_ht_shots - away_ht_shots,
            'ht_sog_diff': home_ht_sog - away_ht_sog,
            'ht_fouls_diff': home_ht_fouls - away_ht_fouls,
            'final_outcome': outcome
        })

        # Dataset 2: Team SOG
        for team_id in [home_team_id, away_team_id]:
            team_sog_data.append({
                'match_id': match_id,
                'team_id': team_id,
                'ht_goals': ht_goals.get(team_id, 0),
                'ht_shots': ht_shots.get(team_id, 0),
                'ht_sog': ht_sog.get(team_id, 0),
                'ht_corners': ht_corners.get(team_id, 0),
                'ht_fouls': ht_fouls.get(team_id, 0),
                'total_shots_on_goal': team_sog_total.get(team_id, 0)
            })

        # Dataset 3: Player SOG
        for team_lineup in lineups:
            for player in team_lineup['lineup']:
                player_id = player['player_id']
                
                # Simple HT features for players
                player_ht_events = ht_events_df[ht_events_df['player_id'] == player_id]
                ht_player_passes = player_ht_events[player_ht_events['type_name'] == 'Pass'].shape[0]
                ht_player_touches = player_ht_events[player_ht_events['type_name'] == 'Ball Receipt*'].shape[0]
                ht_player_dribbles = player_ht_events[player_ht_events['type_name'] == 'Dribble'].shape[0]

                player_sog_data.append({
                    'match_id': match_id,
                    'player_id': player_id,
                    'player_name': player['player_name'],
                    'team_id': team_lineup['team_id'],
                    'ht_passes': ht_player_passes,
                    'ht_touches': ht_player_touches,
                    'ht_dribbles': ht_player_dribbles,
                    'total_shots_on_goal': player_sog_total.get(player_id, 0)
                })

    # Convert lists of dicts to DataFrames
    df_team_outcome = pd.DataFrame(team_outcome_data)
    df_team_sog = pd.DataFrame(team_sog_data)
    df_player_sog = pd.DataFrame(player_sog_data)
    
    return df_team_outcome, df_team_sog, df_player_sog

def main():
    """
    Main function to run the data processing pipeline.
    """
    print("Starting data processing for Ligue 1 2021/2022...")
    
    # 1. Get match IDs for Ligue 1 2021/2022
    competition_name = "Ligue 1"
    season_name = "2021/2022"
    match_ids, match_info = get_match_data_for_competition_season(competition_name, season_name)
    
    # 2. Process data and generate DataFrames
    df_team_outcome, df_team_sog, df_player_sog = process_data(match_ids, match_info)
    
    # 3. Save DataFrames to CSV
    try:
        outcome_path = f'C:/Users/maced/Documents/Projetos/JACKBOT/ligue1_2021_2022_team_outcome.csv'
        team_sog_path = f'C:/Users/maced/Documents/Projetos/JACKBOT/ligue1_2021_2022_team_sog.csv'
        player_sog_path = f'C:/Users/maced/Documents/Projetos/JACKBOT/ligue1_2021_2022_player_sog.csv'

        df_team_outcome.to_csv(outcome_path, index=False)
        print(f"Successfully saved team outcome data to {outcome_path}")
        
        df_team_sog.to_csv(team_sog_path, index=False)
        print(f"Successfully saved team SOG data to {team_sog_path}")

        df_player_sog.to_csv(player_sog_path, index=False)
        print(f"Successfully saved player SOG data to {player_sog_path}")
        
        print("\n--- Verification ---")
        print(f"Team Outcome Shape: {df_team_outcome.shape}")
        print(f"Team SOG Shape: {df_team_sog.shape}")
        print(f"Player SOG Shape: {df_player_sog.shape}")

    except Exception as e:
        print(f"An error occurred during file saving: {e}")


if __name__ == '__main__':
    main()
