from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
 
# Creating a webdriver instance
driver = webdriver.Chrome(r"C:\Users\mohit\Downloads\chromedriver_win32\chromedriver.exe")
# This instance will be used to log into LinkedIn
 
# Opening linkedIn's login page
driver.get("https://linkedin.com/uas/login")
 
# waiting for the page to load
time.sleep(5)
 
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
time.sleep(10) 
job_icon=driver.find_element(By.XPATH, "/html/body/div[5]/header/div/nav/ul/li[3]/a").click()
time.sleep(5)
job_icon=driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div[3]/div/div/main/section/ul/li[1]").click()
time.sleep(20)


#starting to gernerate the json file for the job posted
jobs_per_page_xpath="//div[@class='full-width artdeco-entity-lockup__title ember-view']"
job_titles=driver.find_elements(By.XPATH,jobs_per_page_xpath)
time.sleep(30)
job_title=[]
for elem in job_titles:
    job_title.append(elem.text)
    time.sleep(2)
print(job_title)
