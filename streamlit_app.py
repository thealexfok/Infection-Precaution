import streamlit as st
import pandas as pd

# Load the data with caching to avoid reloading on every interaction
@st.cache
def load_data():
    return pd.read_csv("infection_data.csv")

data = load_data()

# App layout
st.title("Infection Precautions Dictionary")
st.write("Search for infection/condition and view the recommended isolation precautions.")

# Search bar
search_term = st.text_input("Search for an infection or condition", "")

# Filter data based on the search term
if search_term:
    filtered_data = data[data['Infection/Condition'].str.contains(search_term, case=False, na=False)]
    if not filtered_data.empty:
        st.write("### Search Results")
        st.write(filtered_data[['Infection/Condition', 'Type of Precaution', 'Duration of Precaution', 'Precautions/Comments']])
    else:
        st.write("No matching infections found.")
else:
    st.write("Please enter an infection name to search.")

# Expandable section to view all data
with st.expander("View all infections"):
    st.dataframe(data[['Infection/Condition', 'Type of Precaution', 'Duration of Precaution', 'Precautions/Comments']])
