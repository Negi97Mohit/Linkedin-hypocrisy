from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Set up the WebDriver (assuming Chrome in this example)
driver = webdriver.Chrome()

# Open a website
driver.get("https://ww7.gogoanimes.org")

# Find the search input element
search_input = driver.find_element(By.ID, "keyword")

# Enter a search value
search_input.send_keys("TRIGUN (DUB)")

# Wait for the search button to be clickable
search_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "btngui"))
)
time.sleep(3000)


# Click the search button
search_button.click()

# Close the WebDriver
driver.quit()



