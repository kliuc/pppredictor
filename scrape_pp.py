import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


options = uc.ChromeOptions()
# options.add_argument('--headless')\
driver = uc.Chrome(options=options)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

# load page and close popup
driver.get('https://app.prizepicks.com/')
element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div/div/div[3]/button')))
element.click()

# get all available sports leagues
leagues = driver.find_element(By.XPATH, '//*[@id="board"]/div[1]/div/div').find_elements(By.XPATH, '*')
leagues_dict = {league.text: league for league in leagues}

# click on MLB
leagues_dict['MLB'].click()

# get all stats
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'stat-container')))
mlb_stats = element.find_elements(By.XPATH, '*')
mlb_stats_dict = {stat.text: stat for stat in mlb_stats}

# click on Pitcher Strikeouts
mlb_stats_dict['Pitcher Strikeouts'].click()

# get all squares
element = wait.until(EC.presence_of_element_located((By.ID, 'projections')))
squares = element.find_elements(By.CLASS_NAME, 'projection')

for square in squares:
    name = square.find_element(By.CLASS_NAME, 'name').text
    opponent = square.find_element(By.CLASS_NAME, 'opponent').text.split()[1]
    projection = float(square.find_element(By.CLASS_NAME, 'score').text)
    print(name, opponent, projection)

driver.quit()