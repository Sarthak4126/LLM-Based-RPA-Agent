# src/automation/web.py
import time, random
from src.core.logger import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class WebAutomator:
    def __init__(self):
        self.driver = None
        self._setup_driver()

    def _setup_driver(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.maximize_window()
            logger.info("Selenium browser launched with anti-bot detection measures.")
        except Exception as e:
            logger.error(f"Failed to setup Selenium driver: {e}", exc_info=True); raise e

    def search(self, query: str, site: str = "google") -> bool:
        self.driver.get(f'https://www.{site}.com')
        wait = WebDriverWait(self.driver, 10)
        search_box_selector = 'textarea[name="q"]' if site == "google" else 'input[name="search_query"]'
        search_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, search_box_selector)))
        search_box.clear(); search_box.send_keys(query); search_box.send_keys(Keys.RETURN)
        return True

    def click_element(self, selector: str) -> bool:
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        element.click()
        time.sleep(3)
        return True

    def close(self):
        if self.driver: self.driver.quit()