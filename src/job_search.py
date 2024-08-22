import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

class JobSearch:
    def __init__(self, driver, config):
        self.driver = driver
        self.search_terms = config['search_terms']
        self.location = config['location']
        self.date_posted = config['date_posted']
        self.sort_by = config['sort_by']

    def search(self):
        job_listings = []
        for term in self.search_terms:
            try:
                self.driver.get(f"https://www.linkedin.com/jobs/search/?keywords={term}")
                self._apply_filters()
                job_listings.extend(self._get_job_listings())
            except Exception as e:
                logger.error(f"Error searching for term '{term}': {str(e)}")
        return job_listings

    def _apply_filters(self):
        try:
            # Apply location filter
            location_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']"))
            )
            location_input.clear()
            location_input.send_keys(self.location)

            # Apply date posted filter
            date_filter = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{self.date_posted}')]")
            date_filter.click()

            # Apply sort by filter
            sort_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Sort by')]")
            sort_button.click()
            sort_option = self.driver.find_element(By.XPATH, f"//span[contains(text(), '{self.sort_by}')]")
            sort_option.click()

        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Error applying filters: {str(e)}")

    def _get_job_listings(self):
        job_cards = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container"))
        )
        return [card.get_attribute('data-job-id') for card in job_cards]