# import scrapper as sc
import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np

st.set_page_config(layout="wide")

# Loading the csv file into the dataframe
df_main = pd.read_csv("Latest_Jobes.csv")


def main():
    img = Image.open('banner.jpg')
    # img = img.resize((300, 400))
    st.image(img)

    st.title("linkedIn What A Joke ")
    st.write('A dashbord to display why jobs are are to get on linkedIn,  cause they are misleading and not accurate at all')

    job_titles = df_main['job_titles'].tolist()
    selected_job = st.multiselect("Select the job title", job_titles)

    job_type = []
    company_size = []
    salary = []
    job_level = []
    sector = []

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
            # getting the company size
            if 'employees' in cd:
                cs = cd.split('employees', 1)
                company_size.append(cs[0])
                sector.append(cs[1])

    df_main['job_type'] = job_type
    df_main['job_level'] = job_level
    df_main['company_size'] = company_size
    df_main['sector'] = sector
    df_main.drop(['company_type'], axis=1, inplace=True)
    st.write(df_main)


def job_description():
    jds = df_main.job_description.tolist()
    st.write(len(jds))
    counter1 = 0
    counter2 = 0
    for jd in jds:
        if 'Responsibilities' in jd:
            counter1 += 1
        if 'Qualifications' in jd:
            counter2 += 1
    st.write(counter1)
    st.write(counter2)


if __name__ == '__main__':
    main()
    job_description()
