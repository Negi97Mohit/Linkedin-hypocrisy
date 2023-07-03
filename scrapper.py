from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys

import pandas as pd

# Creating a webdriver instance
driver = webdriver.Chrome(
    r"C:\Users\mohit\Downloads\chromedriver_win32\chromedriver.exe")
# This instance will be used to log into LinkedIn

# Opening linkedIn's login page
driver.get("https://linkedin.com/uas/login")

# waiting for the page to load
time.sleep(5)


def main():
    # entering username
    username = driver.find_element(By.ID, "username")

    # In case of an error, try changing the element
    # tag used here.

    # Enter Your Email Address
    username.send_keys("negi.m@northeastern.edu")

    # entering password
    pword = driver.find_element(By.ID, "password")
    # In case of an error, try changing the element
    # tag used here.

    # Enter Your Password
    pword.send_keys("Lonely123)")

    # Clicking on the log in button
    # Format (syntax) of writing XPath -->
    # //tagname[@attribute='value']
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # In case of an error, try changing the
    # XPath used here.
    time.sleep(20)
    job_icon = driver.find_element(
        By.XPATH, "/html/body/div[5]/header/div/nav/ul/li[3]/a").click()

    time.sleep(5)
    job_icon = driver.find_element(
        By.XPATH, "/html/body/div[5]/div[3]/div/div[3]/div/div/main/section/ul/li[1]").click()

    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.END)
    time.sleep(10)

    # starting to gernerate the json file for the job posted
    jobs_per_page_xpath = "//div[@class='full-width artdeco-entity-lockup__title ember-view']"
    job_titles = driver.find_elements(By.XPATH, jobs_per_page_xpath)

    # trying to scroll down the job_list div
    # scroll_elem = driver.find_element(
    #     By.XPATH, "//div[@class='scaffold-layout__list ']")
    # driver.execute_script("arguments[0].scrollIntoView(true);", scroll_elem)
    # time.sleep(10)
    # scroll_elem = driver.find_element(
    #     By.XPATH, "//div[@class='scaffold-layout__list ']")
    # driver.execute_script("arguments[0].scrollIntoView(true);", scroll_elem)
    time.sleep(10)
    job_title = []
    for elem in job_titles:
        job_title.append(elem.text)
        time.sleep(2)

    job_type = []
    company_size = []
    job_description = []
    for elem in job_titles:
        elem.click()
        time.sleep(30)
        job_info_xpath = "//li[@class='jobs-unified-top-card__job-insight']"
        elem_attr = driver.find_elements(
            By.XPATH, job_info_xpath)
        counter = 0
        attr_len = len(elem_attr)
        for ele in elem_attr:
            # if counter == 0:
            print(ele.text)
            #     counter += 1
            # if attr_len > 0 and counter == 1:
            #     company_size.append(ele.text)

    print(job_title)
    # print(job_type)
    # print(company_size)

    # jobs = pd.DataFrame(job_title, columns=['Job_Titles'])
    # print(jobs)
    # return jobs


if __name__ == '__main__':
    main()
