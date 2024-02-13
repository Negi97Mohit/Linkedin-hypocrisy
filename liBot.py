import streamlit as st
from docx import Document
from io import StringIO
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
import logging
import os
import csv
import pandas as pd
import plotly.express as px
import pickle 

class LinkedInBot:
    def __init__(self, delay=5):
        if not os.path.exists("data"):
            os.makedirs("data")
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt)
        self.delay = delay
        logging.info("Starting driver")
        self.driver = webdriver.Chrome()

    def login(self, email, password):
        """Go to LinkedIn and login"""
        logging.info("Logging in")
        self.driver.maximize_window()
        self.driver.get('https://www.linkedin.com/login')
        time.sleep(self.delay)

        self.driver.find_element(By.ID, 'username').send_keys(email)
        self.driver.find_element(By.ID, 'password').send_keys(password)

        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(self.delay)

    def save_cookie(self, path):
        with open(path, 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)

    def load_cookie(self, path):
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def search_linkedin(self, keywords, location, date_posted):
        """Enter keywords into the search bar"""
        logging.info("Searching jobs page")
        self.driver.get("https://www.linkedin.com/jobs/")
        # Search based on keywords, location, and date posted and hit enter
        self.driver.get(f"https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}&f_TPR={date_posted}")
        logging.info("Keyword search successful")
        time.sleep(self.delay)

    def wait(self, t_delay=None):
        """Just easier to build this in here."""
        delay = self.delay if t_delay is None else t_delay
        time.sleep(delay)

    def scroll_to(self, job_list_item):
        """Scroll to the list item in the column and click on it."""
        try:
            # Scroll to the element
            self.driver.execute_script("arguments[0].scrollIntoView();", job_list_item)
            job_list_item.click()
            time.sleep(self.delay)
            logging.info("Clicked on job_list_item")
        except Exception as e:
            logging.error(f"Failed to click on job_list_item: {e}")

    def get_position_data(self, job):
        """Gets the position data for a posting."""
        job_info = job.text.split('\n')
        if len(job_info) < 3:
            logging.warning("Incomplete job information, skipping...")
            return None

        position, company, *details = job_info
        location = details[0] if details else None
        description = self.get_job_description(job)
        application_link = self.get_application_link(job)

        # Extract additional details if available
        company_size, position_level, salary = self.extract_additional_details(job)

        return [position, company, location, description, company_size, position_level, salary, application_link]

    def extract_additional_details(self, job):
        """Extracts additional details like company size, position level, and salary if available."""
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
        """Gets the job description."""
        # Click on the job to view its details
        self.scroll_to(job)

        try:
            description_element = self.driver.find_element(By.CLASS_NAME, "jobs-description")
            description = description_element.text
        except NoSuchElementException:
            description = None

        return description

    def get_application_link(self, job):
        """Gets the job application link."""
        try:
            application_link_element = job.find_element(By.CLASS_NAME, "job-card-search__apply-button-container").find_element(By.TAG_NAME, "a")
            application_link = application_link_element.get_attribute("href")
        except NoSuchElementException:
            application_link = None

        return application_link

    def wait_for_element_ready(self, by, text):
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((by, text)))
        except TimeoutException:
            logging.debug("wait_for_element_ready TimeoutException")
            pass

    def close_session(self):
        """Close the actual session"""
        logging.info("Closing session")
        self.driver.close()

    def run(self, email, password, keywords, location, date_posted):
        if os.path.exists("data/cookies.txt"):
            self.driver.get("https://www.linkedin.com/")
            self.load_cookie("data/cookies.txt")
            self.driver.get("https://www.linkedin.com/")
        else:
            self.login(email=email, password=password)
            self.save_cookie("data/cookies.txt")

        logging.info("Begin LinkedIn keyword search")
        self.search_linkedin(keywords, location, date_posted)
        self.wait()

        # Open the CSV file for writing
        csv_file_path = os.path.join("data", "data.csv")
        with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Position", "Company", "Location", "Description", "Company Size", "Position Level", "Salary", "Application Link"])

            # Scrape pages
            page = 1
            while True:
                # Get the jobs list items to scroll through
                jobs = self.driver.find_elements(By.CLASS_NAME, "occludable-update")
                for job in jobs:
                    job_data = self.get_position_data(job)
                    if job_data:
                        # Unpack job_data into variables
                        position, company, location, description, company_size, position_level, salary, application_link = job_data
                        # Write the job details to the CSV file
                        writer.writerow([position, company, location, description, company_size, position_level, salary, application_link])

                # Go to next page if it exists
                next_button_xpath = f"//button[@aria-label='Page {page + 1}']"
                next_button = self.driver.find_elements(By.XPATH, next_button_xpath)
                if next_button:
                    next_button[0].click()
                    self.wait()
                    page += 1
                else:
                    break  # No more pages to scrape

        logging.info("Done scraping.")
        logging.info("Closing DB connection.")
        self.close_session()

def highlight_words_in_text(text, words_to_highlight):
    highlighted_text = ""
    for word in text.split():
        if word.lower() in words_to_highlight:
            highlighted_text += f"<span style='color: green;'>{word}</span> "
        else:
            highlighted_text += f"<span style='color: red;'>{word}</span> "
    return highlighted_text.strip()
# Define color ranges based on similarity score
def assign_color(similarity):
    if similarity >= 40:
        return 'green'
    elif 35 <= similarity < 40:
        return 'yellow'
    elif 30 <= similarity < 35:
        return 'blue'
    else:
        return 'red'
    
def main():
    st.set_page_config(layout="wide") 
    st.title("LinkedIn Job Analysis")

    col1, col2 = st.columns([1, 1])
    with col1:
        # Scrape LinkedIn Jobs
        st.header("Scrape LinkedIn Jobs")
        st.write("Enter your LinkedIn credentials and search criteria below to scrape job postings.")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        keywords = st.text_input("Keywords")
        location = st.text_input("Location")
        # date_posted = st.selectbox("Date Posted", ["r86400", "r604800", "r2592000"], index=1)
        date_options = {
            "Within the Last Day": "r86400",
            "Within the Last Week": "r604800",
            "Within the Last Month": "r2592000"
        }
        date_posted = st.selectbox("Date Posted", list(date_options.keys()), index=1)
        date_posted = date_options[date_posted]

        if st.button("Scrape Jobs"):
            bot = LinkedInBot()
            bot.run(email, password, keywords, location, date_posted)
            st.success("Job scraping completed!")
        with st.expander("See Scraper Code"):
            code = '''class LinkedInBot:
        def __init__(self, delay=5):
            if not os.path.exists("data"):
                os.makedirs("data")
            log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            logging.basicConfig(level=logging.INFO, format=log_fmt)
            self.delay=delay
            logging.info("Starting driver")
            self.driver = webdriver.Chrome()

        def login(self, email, password):
            """Go to LinkedIn and login"""
            logging.info("Logging in")
            self.driver.maximize_window()
            self.driver.get('https://www.linkedin.com/login')
            time.sleep(self.delay)

            self.driver.find_element(By.ID, 'username').send_keys(email)
            self.driver.find_element(By.ID, 'password').send_keys(password)

            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(self.delay)

        def save_cookie(self, path):
            with open(path, 'wb') as filehandler:
                pickle.dump(self.driver.get_cookies(), filehandler)

        def load_cookie(self, path):
            with open(path, 'rb') as cookiesfile:
                cookies = pickle.load(cookiesfile)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)

        def search_linkedin(self, keywords, location, date_posted):
            """Enter keywords into the search bar"""
            logging.info("Searching jobs page")
            self.driver.get("https://www.linkedin.com/jobs/")
            # Search based on keywords, location, and date posted and hit enter
            self.driver.get(f"https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}&f_TPR={date_posted}")
            logging.info("Keyword search successful")
            time.sleep(self.delay)
        
        def wait(self, t_delay=None):
            """Just easier to build this in here."""
            delay = self.delay if t_delay is None else t_delay
            time.sleep(delay)

        def scroll_to(self, job_list_item):
            """Scroll to the list item in the column and click on it."""
            try:
                # Scroll to the element
                self.driver.execute_script("arguments[0].scrollIntoView();", job_list_item)
                job_list_item.click()
                time.sleep(self.delay)
                logging.info("Clicked on job_list_item")
            except Exception as e:
                logging.error(f"Failed to click on job_list_item: {e}")

        def get_position_data(self, job):
            """Gets the position data for a posting."""
            job_info = job.text.split('\n')
            if len(job_info) < 3:
                logging.warning("Incomplete job information, skipping...")
                return None

            position, company, *details = job_info
            location = details[0] if details else None
            description = self.get_job_description(job)
            application_link = self.get_application_link(job)

            # Extract additional details if available
            company_size, position_level, salary = self.extract_additional_details(job)

            return [position, company, location, description, company_size, position_level, salary, application_link]
    '''
            st.code(code, language='python')
    with col2:
        df = pd.read_csv("data/data.csv")

        # Perform EDA
        st.header("Exploratory Data Analysis")

        # Count of Positions
        st.subheader("Count of Positions")

        # Count positions
        position_counts = df["Position"].value_counts().reset_index()
        position_counts.columns = ['Position', 'Count']

        # Create bar plot using Plotly
        fig = px.bar(position_counts, x='Position', y='Count', title='Count of Positions')
        fig.update_xaxes(tickangle=45)
        fig.update_layout(xaxis_title='Position', yaxis_title='Count')
        st.plotly_chart(fig)

    st.subheader('After scraping upload your resume')

    uploaded_file = st.file_uploader("Choose a DOCX file", type="docx")
    if uploaded_file:
        docx = Document(uploaded_file)
        resume_text = ""
        for paragraph in docx.paragraphs:
            resume_text += paragraph.text + "\n"
        st.write("File contents:")
        with st.expander("See Resume"):
            st.write(resume_text)
            
    if st.button("Similarity Check"):
            df = pd.read_csv("data/data.csv")

            # Perform TF-IDF vectorization
            vectorizer = TfidfVectorizer()
            job_descriptions = df["Description"].fillna("")
            tfidf_matrix = vectorizer.fit_transform(job_descriptions)

            # Compute cosine similarity
            resume_tfidf = vectorizer.transform([resume_text])
            similarity_scores = cosine_similarity(resume_tfidf, tfidf_matrix)[0]

            # Add similarity scores to the dataframe
            df["Similarity (%)"] = similarity_scores * 100
            df.to_csv("data/data.csv", index=False)
            st.success("Similarity check completed and saved to data.csv")

                # Your scraping code and other UI components here...

    st.subheader("View CSV File")

    # Button to display CSV file
    if st.button("Show CSV File"):
        df = pd.read_csv("data/data.csv")
        st.write(df)
        fig = px.scatter(df, x="Position", y="Similarity (%)", title="Similarity Scores for Job Positions",height=800)

        # Customize marker colors based on similarity score
        colors = ['green' if val > 40 else 'red' for val in df["Similarity (%)"]]
        fig.update_traces(marker=dict(color=colors), mode="markers")

        fig.update_layout(xaxis_tickangle=-45, xaxis_title="Position", yaxis_title="Similarity (%)")
        st.plotly_chart(fig, use_container_width=True)


    selected_positions = st.multiselect("Select Position", df["Position"].unique())
    if selected_positions:
        for position in selected_positions:
            st.subheader(f"Job Position: {position}")
            job_data = df[df["Position"] == position].iloc[0]
            for column in df.columns:
                st.markdown(f"<span style='background-color: #f4a261; padding: 2px 4px; border-radius: 4px;'>{column}</span>: {job_data[column]}", unsafe_allow_html=True)
            st.write("---")

if __name__ == "__main__":
    main()
