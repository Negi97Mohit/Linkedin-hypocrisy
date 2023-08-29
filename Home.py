# Importing required libraries
import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import re

# Set the layout of the Streamlit page to "wide"
st.set_page_config(layout="wide")

# Load the job data from the CSV file into the DataFrame
df_main = pd.read_csv("Latest_Jobs.csv")

# Main function for the Streamlit web app


def main():
    # Load and display the banner image
    img = Image.open('banner.jpg')
    st.image(img)

    # Set the title and description of the Streamlit app
    st.title("linkedIn What A Joke")
    st.write('A dashboard to display why jobs are hard to get on LinkedIn because they are misleading and not accurate at all')

    # Get the list of job titles from the DataFrame
    job_titles = df_main['job_titles'].tolist()
    # Allow users to select one or more job titles using a multi-select dropdown
    selected_job = st.multiselect("Select the job title", job_titles)

    # Lists to store extracted job information
    job_type = []
    company_size = []
    salary = []
    job_level = []
    sector = []

    # Extract job-related information from the 'company_type' column in the DataFrame
    company_type = []
    df_ct = df_main.company_type.tolist()
    for cds in df_ct:
        res = cds.strip('][').split(', ')
        company_type.append(res)

    for cds in company_type:
        for cd in cds:
            # Getting the type and level of the job
            if 'time' in cd:
                job_type.append(cd)
                if 'level' in cd:
                    job_level.append(cd)
                else:
                    job_level.append(np.nan)
            # Getting the company size
            if 'employees' in cd:
                cs = cd.split('employees', 1)
                company_size.append(cs[0])
                sector.append(cs[1])

    # Create new columns in the DataFrame to store the extracted job information
    df_main['job_type'] = job_type
    df_main['job_level'] = job_level
    df_main['company_size'] = company_size
    df_main['sector'] = sector
    df_main.drop(['company_type'], axis=1, inplace=True)


# Function to improve job descriptions
def job_description():
    # Get the list of job descriptions from the DataFrame
    jds = df_main.job_description.tolist()
    # Lists to store key skills and responsibilities extracted from the job descriptions
    responsibilities = []
    skills = []

    # Keywords used as delimiters to split job descriptions and extract key information
    res_keys = ['Responsibilities', 'Your challenge', 'What you will do:']
    skills_key = ['Qualifications', 'ideal candidate ',
                  'What You’ll Need', 'Skills']

    for jd in jds:
        status = False
        for rs in res_keys:
            for sk in skills_key:
                if status == False:
                    # Split the job description using the delimiters and extract responsibilities and skills
                    if rs in jd and sk in jd:
                        splited = re.split(rs + '|' + sk, jd)
                        responsibilities.append(splited[1])
                        skills.append(splited[2])
                        status = True

    # Add new columns in the DataFrame to store the extracted responsibilities and skills
    df_main['skills'] = skills
    df_main['responsibilities'] = responsibilities
    df_main.drop(['job_description'], axis=1, inplace=True)

    # Display the DataFrame with improved job descriptions
    st.write(df_main)
    get_csize(df_main)


def get_csize(df_main):
    df_main['Min Employee'] = ''
    df_main['Max Employee'] = ''
    curr_val = df_main['company_size'].tolist()
    counter = 0
    for val in curr_val:
        val = re.sub("[,]", "", val)
        st.write(val)
        # getting numbers from string
        temp = re.findall(r'\d+', val)
        res = list(map(int, temp))
        df_main['Min Employee'][counter] = res[0]
        if len(res) != 1:
            df_main['Max Employee'][counter] = res[1]
        else:
            df_main['Max Employee'][counter] = np.nan

        counter += 1
    df_main.drop(['company_size'], inplace=True, axis=1)
    st.write(df_main)


if __name__ == '__main__':
    # Call the main and job_description functions
    main()
    job_description()
