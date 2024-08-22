import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

logger = logging.getLogger(__name__)

class JobApply:
    def __init__(self, driver, config):
        self.driver = driver
        self.easy_apply_only = config['easy_apply_only']
        self.run_non_stop = config['run_non_stop']
        self.max_retries = config.get('max_retries', 3)
        self.retry_delay = config.get('retry_delay', 5)
        self.answers = config.get('default_answers', {})

    def apply_to_jobs(self, job_listings):
        for job_id in job_listings:
            try:
                self._apply_to_job(job_id)
            except Exception as e:
                logger.error(f"Error applying to job {job_id}: {str(e)}")
                if not self.run_non_stop:
                    break

    def _apply_to_job(self, job_id):
        retries = 0
        while retries < self.max_retries:
            try:
                self.driver.get(f"https://www.linkedin.com/jobs/view/{job_id}")
                
                apply_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".jobs-apply-button"))
                )
                apply_button.click()

                if self.easy_apply_only and "Easy Apply" not in apply_button.text:
                    logger.info(f"Skipping job {job_id} as it's not Easy Apply")
                    return

                self._fill_application_form()
                self._submit_application()
                
                logger.info(f"Successfully applied to job {job_id}")
                break
            
            except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
                logger.warning(f"Attempt {retries + 1} failed for job {job_id}: {str(e)}")
                retries += 1
                if retries < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"Failed to apply to job {job_id} after {self.max_retries} attempts")

    def _fill_application_form(self):
        while True:
            try:
                # Handle different types of questions
                self._handle_text_inputs()
                self._handle_selects()
                self._handle_radios()
                self._handle_checkboxes()
                self._handle_textareas()

                # Click the Next button if it exists
                next_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']")
                if next_button.is_enabled():
                    next_button.click()
                    time.sleep(1)  # Wait for the next page to load
                else:
                    break  # No more pages, form is complete
            except NoSuchElementException:
                break  # No more questions to answer

    def _handle_text_inputs(self):
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
        for input_field in inputs:
            label = self._get_label_for_element(input_field)
            if label in self.answers:
                input_field.clear()
                input_field.send_keys(self.answers[label])

    def _handle_selects(self):
        selects = self.driver.find_elements(By.TAG_NAME, "select")
        for select_field in selects:
            label = self._get_label_for_element(select_field)
            if label in self.answers:
                Select(select_field).select_by_visible_text(self.answers[label])

    def _handle_radios(self):
        radio_groups = self.driver.find_elements(By.CSS_SELECTOR, "fieldset")
        for group in radio_groups:
            legend = group.find_element(By.TAG_NAME, "legend").text
            if legend in self.answers:
                radio = group.find_element(By.XPATH, f".//input[@value='{self.answers[legend]}']")
                radio.click()

    def _handle_checkboxes(self):
        checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        for checkbox in checkboxes:
            label = self._get_label_for_element(checkbox)
            if label in self.answers:
                if self.answers[label] and not checkbox.is_selected():
                    checkbox.click()
                elif not self.answers[label] and checkbox.is_selected():
                    checkbox.click()

    def _handle_textareas(self):
        textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
        for textarea in textareas:
            label = self._get_label_for_element(textarea)
            if label in self.answers:
                textarea.clear()
                textarea.send_keys(self.answers[label])

    def _get_label_for_element(self, element):
        try:
            label_id = element.get_attribute("id")
            label = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{label_id}']")
            return label.text
        except NoSuchElementException:
            return ""

    def _submit_application(self):
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Submit application']"))
        )
        submit_button.click()
        
        # Wait for confirmation
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-inline-feedback--success"))
            )
            logger.info("Application submitted successfully")
        except TimeoutException:
            logger.warning("Couldn't confirm if the application was submitted successfully")