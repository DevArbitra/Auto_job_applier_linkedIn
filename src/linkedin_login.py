from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LinkedInLogin:
    def __init__(self, config):
        self.username = config['username']
        self.password = config['password']
        
    def login(self):
        driver = webdriver.Chrome()  # Or whichever browser you're using
        driver.get("https://www.linkedin.com/login")
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        
        driver.find_element(By.ID, "username").send_keys(self.username)
        driver.find_element(By.ID, "password").send_keys(self.password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        WebDriverWait(driver, 10).until(EC.url_contains("feed"))
        
        return driver