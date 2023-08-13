import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class PPScraper:
    def __init__(self):
        self.options = uc.ChromeOptions()
        # self.options.add_argument('--headless')
        self.driver = uc.Chrome(options=self.options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

        # load PP and close popup
        self.driver.get('https://app.prizepicks.com/')
        popup = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div/div/div[3]/button')))
        popup.click()

    def _get_leagues(self):
        leagues = self.driver.find_element(By.XPATH, '//*[@id="board"]/div[1]/div/div').find_elements(By.XPATH, '*')
        leagues_dict = {league.text: league for league in leagues}
        return leagues_dict
    
    def _get_stats(self):
        stat_container = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "stat-container")))
        stats = stat_container.find_elements(By.XPATH, '*')
        stats_dict = {stat.text: stat for stat in stats}
        return stats_dict
    
    def _get_projections(self):
        element = self.wait.until(EC.presence_of_element_located((By.ID, 'projections')))
        squares = element.find_elements(By.CLASS_NAME, 'projection')

        projections = []
        for square in squares:
            name = square.find_element(By.CLASS_NAME, 'name').text
            opponent = square.find_element(By.CLASS_NAME, 'opponent').text.split()[1]
            projection = float(square.find_element(By.CLASS_NAME, 'score').text)
            projections.append((name, opponent, projection))

        self.driver.quit()
        return projections

    def scrape(self, sport, stat):
        leagues_dict = self._get_leagues()
        if sport in leagues_dict:
            leagues_dict[sport].click()
            time.sleep(1)
            stats_dict = self._get_stats()
            if stat in stats_dict:
                stats_dict[stat].click()
                return self._get_projections()
            else:
                self.driver.quit()
                raise Exception(f'No stat "{stat}" today :(')
        else:
            self.driver.quit()
            raise Exception(f'No sport "{sport}" today :(')


if __name__ == '__main__':
    pp_scraper = PPScraper()
    print(pp_scraper.scrape('LoL', 'MAP 5 Kills'))