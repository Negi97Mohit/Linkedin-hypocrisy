# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import logging
import pickle
import os
import csv

class LinkedInBot:
    def __init__(self, delay=5):
        # Creating 'data' directory if not exists
        if not os.path.exists("data"):
            os.makedirs("data")
        # Configuring logging
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt)
        self.delay = delay
        logging.info("Starting driver")
        self.driver = webdriver.Chrome()

    def login(self, email, password):
        """Log into LinkedIn."""
        # Maximizing window and navigating to LinkedIn login page
        logging.info("Logging in")
        self.driver.maximize_window()
        self.driver.get('https://www.linkedin.com/login')
        time.sleep(self.delay)

        # Entering login credentials and submitting
        self.driver.find_element(By.ID, 'username').send_keys(email)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(self.delay)

    def save_cookie(self, path):
        """Save browser cookies to a file."""
        with open(path, 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)

    def load_cookie(self, path):
        """Load browser cookies from a file."""
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def search_linkedin(self, keywords, location):
        """Search for jobs on LinkedIn based on keywords and location."""
        logging.info("Searching jobs page")
        self.driver.get("https://www.linkedin.com/jobs/")
        # Enter keywords and location into search bar
        self.driver.get(
            f"https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}"
        )
        logging.info("Keyword search successful")
        time.sleep(self.delay)
    
    def wait(self, t_delay=None):
        """Wait for a specified delay."""
        delay = self.delay if t_delay == None else t_delay
        time.sleep(delay)

    def scroll_to(self, job_list_item):
        """Scroll to a job list item."""
        try:
            # Scroll to the element
            self.driver.execute_script("arguments[0].scrollIntoView();", job_list_item)
            job_list_item.click()
            time.sleep(self.delay)
            logging.info("Clicked on job_list_item")
        except Exception as e:
            logging.error(f"Failed to click on job_list_item: {e}")

    def get_position_data(self, job):
        """Extract position data from a job listing."""
        job_info = job.text.split('\n')
        if len(job_info) < 3:
            logging.warning("Incomplete job information, skipping...")
            return None

        position, company, *details = job_info
        location = details[0] if details else None
        description = self.get_job_description(job)

        # Extract additional details if available
        company_size, position_level, salary = self.extract_additional_details(job)

        return [position, company, location, description, company_size, position_level, salary]

    def extract_additional_details(self, job):
        """Extract additional details like company size, position level, and salary."""
        company_size = None
        position_level = None
        salary = None

        try:
            additional_info = job.find_element(By.CLASS_NAME, "job-card-search__company-size").text
            if "employees" in additional_info:
                company_size = additional_info.strip()
        except NoSuchElementException:
            pass

        try:
            position_level = job.find_element(By.CLASS_NAME, "job-card-search__badge").text
        except NoSuchElementException:
            pass

        try:
            salary = job.find_element(By.CLASS_NAME, "job-card-search__salary").text
        except NoSuchElementException:
            pass

        return company_size, position_level, salary

    def get_job_description(self, job):
        """Get the job description."""
        # Click on the job to view its details
        self.scroll_to(job)
        
        try:
            description_element = self.driver.find_element(By.CLASS_NAME, "jobs-description")
            description = description_element.text
        except NoSuchElementException:
            description = None

        return description

    def wait_for_element_ready(self, by, text):
        """Wait for an element to be ready."""
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((by, text)))
        except TimeoutException:
            logging.debug("wait_for_element_ready TimeoutException")
            pass

    def close_session(self):
        """Close the Selenium session."""
        logging.info("Closing session")
        self.driver.close()

    def run(self, email, password, keywords, location):
        if os.path.exists("data/cookies.txt"):
            self.driver.get("https://www.linkedin.com/")
            self.load_cookie("data/cookies.txt")
            self.driver.get("https://www.linkedin.com/")
        else:
            self.login(email=email, password=password)
            self.save_cookie("data/cookies.txt")

        logging.info("Begin LinkedIn keyword search")
        self.search_linkedin(keywords, location)
        self.wait()

        # Open the CSV file for writing
        with open("data/data.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Position", "Company", "Location", "Description", "Company Size", "Position Level", "Salary"])

            # Scrape pages, only do first 8 pages since after that the data isn't well suited for me anyways
            for page in range(2, 4):
                # Get the jobs list items to scroll through
                jobs = self.driver.find_elements(By.CLASS_NAME, "occludable-update")
                for job in jobs:
                    job_data = self.get_position_data(job)
                    if job_data:
                        # Unpack job_data into variables
                        position, company, location, description, company_size, position_level, salary = job_data
                        # Write the job details to the CSV file
                        writer.writerow([position, company, location, description, company_size, position_level, salary])

                # Go to next page
                next_button_xpath = f"//button[@aria-label='Page {page}']"
                next_button = self.driver.find_element(By.XPATH, next_button_xpath)
                next_button.click()
                self.wait()

        logging.info("Done scraping.")
        logging.info("Closing DB connection.")
        self.close_session()

if __name__ == "__main__":
    # Define login credentials
    email = "negi.m@northeastern.edu"
    password = "Lonely123)"
    # Instantiate and run the LinkedInBot
    bot = LinkedInBot()
    bot.run(email, password, "Data Analyst", "New York")


