import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    st.title("LinkedIn Job Analysis")

    # Load the CSV data
    df = pd.read_csv("data/data.csv")

    # Perform EDA
    st.header("Exploratory Data Analysis")

    # Count of Positions
    st.subheader("Count of Positions")
    position_counts = df["Position"].value_counts()
    fig_position_counts, ax = plt.subplots()
    sns.barplot(x=position_counts.index, y=position_counts.values, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax.set_xlabel("Position")
    ax.set_ylabel("Count")
    ax.set_title("Count of Positions")
    st.pyplot(fig_position_counts)

if __name__ == "__main__":
    main()
