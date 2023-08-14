import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from scrape_pp import PPScraper
import get_mlb_data


pp_scraper = PPScraper()
strikeout_projections = pp_scraper.scrape(sport='MLB', stat='Hitter Fantasy Score')

print(strikeout_projections)