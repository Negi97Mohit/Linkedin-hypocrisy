import streamlit as st
import pandas as pd
import plotly.express as px
from linkedin_scraper import LinkedInBot

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

    st.subheader("View CSV File")

    # Button to display CSV file
    if st.button("Show CSV File"):
        df = pd.read_csv("data/data.csv")
        st.write(df)

if __name__ == "__main__":
    main()
