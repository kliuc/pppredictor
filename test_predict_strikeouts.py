import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from scrape_pp import PPScraper
import get_mlb_data


pp_scraper = PPScraper()
strikeout_projections = pp_scraper.scrape(sport='MLB', stat='Pitcher Strikeouts')

name = strikeout_projections[0][0]
projection = strikeout_projections[0][2]
teams_hitting = get_mlb_data.teams_hitting()
pitcher_gamelogs = get_mlb_data.pitcher_gamelogs(name)

for index, row in pitcher_gamelogs.iterrows():
    opp_stats = teams_hitting.query(f'season == {row["season"]} and team_id == {row["opp_id"]}')
    pitcher_gamelogs.at[index, 'opp_strikeouts'] = float(opp_stats['strikeouts_game'])
    pitcher_gamelogs.at[index, 'opp_hits'] = float(opp_stats['hits_game'])

print(pitcher_gamelogs)

X = pitcher_gamelogs[['hits', 'number_of_pitches', 'batters_faced', 'strikes', 'home', 'opp_strikeouts', 'opp_hits']]
y = pitcher_gamelogs['strikeouts'] > projection
model = LogisticRegression(max_iter=1000)
print(X, y)
model.fit(X, y)

home, opp_id = get_mlb_data.next_game(name)
games_last5 = pitcher_gamelogs[['hits', 'number_of_pitches', 'batters_faced', 'strikes']].apply(np.mean)
games_last5['home'] = home
opp_stats = teams_hitting.query(f'season == 2023 and team_id == {opp_id}')
games_last5['opp_strikeouts'] = float(opp_stats['strikeouts_game'])
games_last5['opp_hits'] = float(opp_stats['hits_game'])

print(games_last5)
print(name, projection)
print(model.predict_proba(pd.DataFrame(games_last5).transpose()))