import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import statsapi


mlb_team_ids = {'ARI': 109, 'ATL': 144, 'BAL': 110, 'BOS': 111, 'CHC': 112, 'CHW': 145, 'CWS': 145, 'CIN': 113, 'CLE': 114, 'COL': 115, 'DET': 116,
                'MIA': 146, 'HOU': 117, 'KAN': 118, 'KC': 118, 'LAA': 108, 'LAD': 119, 'MIL': 158, 'MIN': 142, 'NYM': 121, 'NYY': 147, 'OAK': 133,
                'PHI': 143, 'PIT': 134, 'SD': 135, 'SF': 137, 'SEA': 136, 'STL': 138, 'TB': 139, 'TEX': 140, 'TOR': 141, 'WAS': 120, 'WSH': 120}

def get_games_data(name):
    id = statsapi.lookup_player(name)[0]['id']
    stats = statsapi.get('person', {'personId': id, 'hydrate': 'stats(group=pitching,type=gameLog,seasons=[2018,2019,2020,2021,2022,2023])'})
    game_logs = stats['people'][0]['stats'][0]['splits']

    games_data = []
    opp_memo = {}

    for log in game_logs:
        stat = log['stat']
        strikeouts = stat['strikeOuts']
        hits = stat['hits']
        number_of_pitches = stat['numberOfPitches']
        batters_faced = stat['battersFaced']
        strikes = stat['strikes']
        home = log['isHome']

        opp_id = log['opponent']['id']
        season = log['season']
        if (opp_id, season) not in opp_memo:
            opp_stats = statsapi.get('team_stats', {'teamId': opp_id, 'season': season, 'sportIds': 1, 'group': 'hitting', 'stats': 'season'})['stats'][0]['splits'][0]['stat']
            opp_num_games = opp_stats['gamesPlayed']
            opp_strikouts_game = opp_stats['strikeOuts'] / opp_num_games
            opp_hits_game = opp_stats['hits'] / opp_num_games
            opp_memo[(opp_id, season)] = (opp_strikouts_game, opp_hits_game)

        games_data.append((strikeouts, hits, number_of_pitches, batters_faced, strikes, home, *opp_memo[(opp_id, season)]))

    games_df = pd.DataFrame(games_data, columns=['strikeouts', 'hits', 'number_of_pitches', 'batters_faced', 'strikes', 'home', 'opp_strikouts_game', 'opp_hits_game'])
    
    return games_df