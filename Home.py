# import scrapper as sc
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("LinkedIn Hypocrisy")
st.write('A dashbord to display why jobs are are to get on linkedIn,  cause they are misleading and not accurate at all')


df_main = pd.read_csv("Latest_Jobes.csv")
st.write(df_main)

job_titles = df_main['job_titles'].tolist()
selected_job = st.multiselect("Select the job title", job_titles)

job_type = []
company_size = []
salary = []


for cds in df_main.company_type.tolist():
    st.write(cds)
    for cd in str(cds):
        pass
        # if 'time' in cd:
        #     st.write(cd)
        st.write(cd)
