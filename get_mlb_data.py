import numpy as np
import pandas as pd
import statsapi


def teams_hitting(seasons=[2018, 2019, 2020, 2021, 2022, 2023]):
    teams_hitting_list = []

    for season in seasons:
        teams_season = statsapi.get('teams_stats', {'season': season, 'sportIds': 1, 'group': 'hitting', 'stats': 'season'})['stats'][0]['splits']
        for team in teams_season:
            team_id = team['team']['id']
            team_stat = team['stat']
            num_games = team_stat['gamesPlayed']
            strikeouts_game = team_stat['strikeOuts'] / num_games
            hits_game = team_stat['hits'] / num_games
            teams_hitting_list.append({'season': season, 'team_id': team_id, 'strikeouts_game': strikeouts_game, 'hits_game': hits_game})

    teams_hitting_df = pd.DataFrame(teams_hitting_list)
    return teams_hitting_df

def pitcher_gamelogs(name):
    id = statsapi.lookup_player(name)[0]['id']
    stats = statsapi.get('person', {'personId': id, 'hydrate': 'stats(group=pitching,type=gameLog,seasons=[2018,2019,2020,2021,2022,2023])'})
    game_logs = stats['people'][0]['stats'][0]['splits']

    games_data = []

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
        games_data.append((strikeouts, hits, number_of_pitches, batters_faced, strikes, home, opp_id, season))

    games_df = pd.DataFrame(games_data, columns=['strikeouts', 'hits', 'number_of_pitches', 'batters_faced', 'strikes', 'home', 'opp_id', 'season'])
    return games_df

def next_game(name):
    team_id = statsapi.lookup_player(name)[0]['currentTeam']['id']
    next_game_id = statsapi.next_game(team_id)
    game_data = statsapi.schedule(game_id=next_game_id)[0]

    home = game_data['home_id'] == team_id
    if home:
        opp_id = game_data['away_id']
    else:
        opp_id = game_data['home_id']

    return home, opp_id